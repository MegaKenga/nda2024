from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

from django.conf import settings
from django.db import connection
from django.db.models import Q
from django.utils import timezone
from PIL import Image

from catalog.models import Brand, Category, Product
from core.models import MainPageInfoBlock
from files.models import ModelImage

SOURCE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff'}
SKIP_DIRS = {'cache', '.git', '__pycache__'}
IMAGE_FIELD_MODELS = (
    (Brand, 'logo'),
    (Category, 'logo'),
    (Product, 'logo'),
    (ModelImage, 'image'),
    (MainPageInfoBlock, 'block_image'),
)
CKEDITOR_FIELDS = ('short_description', 'full_description', 'characteristics')

LogCallback = Callable[[str, str], None]


@dataclass
class ConversionStats:
    scanned: int = 0
    converted: int = 0
    skipped: int = 0
    failed: int = 0
    saved_bytes: int = 0
    db_image_fields: int = 0
    db_text_fields: int = 0
    deleted_originals: int = 0
    errors: list[str] = field(default_factory=list)


StatsCallback = Callable[[ConversionStats], None]


@dataclass
class OptimizerOptions:
    media_root: str = ''
    quality: int = 82
    max_width: int = 2560
    dry_run: bool = False
    keep_originals: bool = False
    skip_db: bool = False
    skip_files: bool = False


def normalize_rel_path(path: str) -> str:
    return path.replace('\\', '/').lstrip('/')


def build_replacement_variants(old_rel: str, new_rel: str) -> list[tuple[str, str]]:
    from urllib.parse import quote, unquote

    old_rel = normalize_rel_path(old_rel)
    new_rel = normalize_rel_path(new_rel)
    pairs: list[tuple[str, str]] = []

    def add_pair(old_value: str, new_value: str):
        if old_value and old_value not in {pair[0] for pair in pairs}:
            pairs.append((old_value, new_value))

    add_pair(old_rel, new_rel)

    for prefix in ('/media/', 'media/'):
        add_pair(f'{prefix}{old_rel}', f'{prefix}{new_rel}')
        add_pair(f'{prefix}{quote(old_rel, safe="/")}', f'{prefix}{quote(new_rel, safe="/")}')

    decoded = unquote(old_rel)
    if decoded != old_rel:
        add_pair(decoded, new_rel)
        for prefix in ('/media/', 'media/'):
            add_pair(f'{prefix}{decoded}', f'{prefix}{new_rel}')
            add_pair(f'{prefix}{quote(decoded, safe="/")}', f'{prefix}{quote(new_rel, safe="/")}')

    pairs.sort(key=lambda item: len(item[0]), reverse=True)
    return pairs


def replace_path_variants(text: str, old_rel: str, new_rel: str) -> tuple[str, int]:
    if not text:
        return text, 0

    updated = text
    replacements = 0
    for old_variant, new_variant in build_replacement_variants(old_rel, new_rel):
        count = updated.count(old_variant)
        if count:
            updated = updated.replace(old_variant, new_variant)
            replacements += count

    return updated, replacements


def build_all_replacement_pairs(mapping: dict[str, str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()

    for old_rel, new_rel in mapping.items():
        for old_variant, new_variant in build_replacement_variants(old_rel, new_rel):
            if old_variant in seen:
                continue
            seen.add(old_variant)
            pairs.append((old_variant, new_variant))

    pairs.sort(key=lambda item: len(item[0]), reverse=True)
    return pairs


def apply_all_replacements(text: str, pairs: list[tuple[str, str]]) -> tuple[str, int]:
    if not text or not pairs:
        return text, 0

    updated = text
    replacements = 0
    for old_variant, new_variant in pairs:
        if old_variant not in updated:
            continue
        count = updated.count(old_variant)
        updated = updated.replace(old_variant, new_variant)
        replacements += count

    return updated, replacements


BULK_BATCH_SIZE = 500


class JobCancelledError(Exception):
    """Оптимизация остановлена пользователем или сервером."""


def format_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f'{num_bytes} B'
    if num_bytes < 1024 * 1024:
        return f'{num_bytes / 1024:.1f} KB'
    return f'{num_bytes / (1024 * 1024):.1f} MB'


class MediaWebpOptimizer:
    def __init__(
        self,
        options: OptimizerOptions,
        log: LogCallback | None = None,
        should_stop: Callable[[], bool] | None = None,
        on_stats: StatsCallback | None = None,
    ):
        self.options = options
        self.log = log or (lambda message, level='info': None)
        self.should_stop = should_stop or (lambda: False)
        self.on_stats = on_stats
        self.stats = ConversionStats()

    def _emit_stats(self):
        if self.on_stats:
            self.on_stats(self.stats)

    def _check_stop(self):
        if self.should_stop():
            raise JobCancelledError()

    def run(self) -> ConversionStats:
        media_root = Path(self.options.media_root or settings.MEDIA_ROOT).resolve()
        if not media_root.is_dir():
            self._log(f'Каталог media не найден: {media_root}', 'error')
            return self.stats

        self._log(f'MEDIA_ROOT: {media_root}')
        self._log(f'Режим: {"DRY-RUN" if self.options.dry_run else "ЗАПИСЬ"}')
        self._log(
            f'Параметры: quality={self.options.quality}, '
            f'max_width={self.options.max_width}, '
            f'keep_originals={self.options.keep_originals}'
        )

        mapping: dict[str, str] = {}
        if not self.options.skip_files:
            mapping = self._convert_files(media_root)
        else:
            mapping = self._build_existing_webp_mapping(media_root)

        if not self.options.skip_db and mapping:
            self._check_stop()
            self._update_database(mapping)

        if not self.options.dry_run:
            self._check_stop()
            self._clear_thumbnail_cache(media_root)

        self._print_summary()
        return self.stats

    def _log(self, message: str, level: str = 'info'):
        self.log(message, level)

    def _convert_files(self, media_root: Path) -> dict[str, str]:
        mapping: dict[str, str] = {}
        self._log('Сканирование файлов в media/...', 'info')

        for file_path in sorted(media_root.rglob('*')):
            self._check_stop()
            if not file_path.is_file():
                continue

            rel_parts = file_path.relative_to(media_root).parts
            if any(part in SKIP_DIRS for part in rel_parts):
                continue

            extension = file_path.suffix.lower()
            if extension not in SOURCE_EXTENSIONS:
                continue

            self.stats.scanned += 1
            if self.stats.scanned == 1 or self.stats.scanned % 50 == 0:
                self._log(
                    f'Прогресс: просмотрено {self.stats.scanned}, '
                    f'конвертировано {self.stats.converted}, '
                    f'пропущено {self.stats.skipped}',
                    'info',
                )
                self._emit_stats()
            rel_old = normalize_rel_path(str(file_path.relative_to(media_root)))
            rel_new = normalize_rel_path(str(file_path.with_suffix('.webp').relative_to(media_root)))
            dst_path = media_root / rel_new

            if dst_path.exists() and dst_path.stat().st_mtime >= file_path.stat().st_mtime:
                mapping[rel_old] = rel_new
                self.stats.skipped += 1
                self._log(f'Пропуск (webp уже есть): {rel_old}', 'skip')
                continue

            try:
                original_size = file_path.stat().st_size
                if self.options.dry_run:
                    mapping[rel_old] = rel_new
                    self.stats.converted += 1
                    self._log(f'Будет конвертировано: {rel_old} -> {rel_new}', 'plan')
                    continue

                saved_size = self._save_as_webp(file_path, dst_path)
                mapping[rel_old] = rel_new
                self.stats.converted += 1
                self.stats.saved_bytes += max(0, original_size - saved_size)
                self._log(
                    f'Конвертировано: {rel_old} -> {rel_new} '
                    f'({format_size(original_size)} -> {format_size(saved_size)})',
                    'success',
                )

                if not self.options.keep_originals:
                    file_path.unlink()
                    self.stats.deleted_originals += 1

                if self.stats.converted % 100 == 0:
                    import gc
                    gc.collect()
            except Exception as exc:
                self.stats.failed += 1
                message = f'{rel_old}: {exc}'
                self.stats.errors.append(message)
                self._log(message, 'error')

        return mapping

    def _build_existing_webp_mapping(self, media_root: Path) -> dict[str, str]:
        mapping: dict[str, str] = {}

        for file_path in sorted(media_root.rglob('*')):
            self._check_stop()
            if not file_path.is_file():
                continue

            rel_parts = file_path.relative_to(media_root).parts
            if any(part in SKIP_DIRS for part in rel_parts):
                continue

            extension = file_path.suffix.lower()
            if extension not in SOURCE_EXTENSIONS:
                continue

            rel_old = normalize_rel_path(str(file_path.relative_to(media_root)))
            rel_new = normalize_rel_path(str(file_path.with_suffix('.webp').relative_to(media_root)))
            if (media_root / rel_new).exists():
                mapping[rel_old] = rel_new
                self.stats.scanned += 1

        return mapping

    def _save_as_webp(self, src_path: Path, dst_path: Path) -> int:
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        with Image.open(src_path) as image:
            image.load()

            if self.options.max_width and image.width > self.options.max_width:
                ratio = self.options.max_width / float(image.width)
                new_size = (self.options.max_width, max(1, int(image.height * ratio)))
                image = image.resize(new_size, Image.Resampling.LANCZOS)

            if image.mode in ('RGBA', 'LA') or (
                image.mode == 'P' and 'transparency' in image.info
            ):
                image = image.convert('RGBA')
            elif image.mode != 'RGB':
                image = image.convert('RGB')

            save_kwargs = {
                'format': 'WEBP',
                'quality': self.options.quality,
                'method': 6,
            }
            if image.mode == 'RGBA':
                save_kwargs['lossless'] = False

            image.save(dst_path, **save_kwargs)

        return dst_path.stat().st_size

    def _update_database(self, mapping: dict[str, str]):
        if not mapping:
            self._log('Нет путей для обновления в БД.', 'warn')
            return

        self._log(f'Обновление ImageField в PostgreSQL ({len(mapping)} путей)...')
        self._bulk_update_image_fields(mapping)
        self._update_ckeditor_fields(mapping)

    def _bulk_update_image_fields(self, mapping: dict[str, str]):
        mapping_keys = list(mapping.keys())

        for model, field_name in IMAGE_FIELD_MODELS:
            updated_rows = 0
            pending: list = []

            for key_chunk in self._chunked(mapping_keys, 1000):
                queryset = (
                    model.objects
                    .exclude(**{f'{field_name}__exact': ''})
                    .exclude(**{f'{field_name}__isnull': True})
                    .filter(**{f'{field_name}__in': key_chunk})
                    .only('pk', field_name)
                )

                for obj in queryset.iterator(chunk_size=2000):
                    self._check_stop()
                    current = normalize_rel_path(getattr(obj, field_name).name)
                    new_value = mapping.get(current)
                    if not new_value:
                        continue

                    if self.options.dry_run:
                        updated_rows += 1
                        continue

                    setattr(obj, field_name, new_value)
                    pending.append(obj)

                    if len(pending) >= BULK_BATCH_SIZE:
                        model.objects.bulk_update(pending, [field_name], batch_size=BULK_BATCH_SIZE)
                        updated_rows += len(pending)
                        self._log(
                            f'{model.__name__}.{field_name}: обновлено {updated_rows}...',
                            'db',
                        )
                        pending = []

            if pending and not self.options.dry_run:
                model.objects.bulk_update(pending, [field_name], batch_size=BULK_BATCH_SIZE)
                updated_rows += len(pending)

            self.stats.db_image_fields += updated_rows
            if updated_rows:
                self._log(f'{model.__name__}.{field_name}: итого {updated_rows} записей', 'db')

    def _update_ckeditor_fields(self, mapping: dict[str, str]):
        pairs = build_all_replacement_pairs(mapping)
        if not pairs:
            return

        media_query = Q()
        for field_name in CKEDITOR_FIELDS:
            for marker in ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '/media/'):
                media_query |= Q(**{f'{field_name}__icontains': marker})

        queryset = Product.objects.filter(media_query).only('pk', *CKEDITOR_FIELDS)
        total = queryset.count()
        self._log(f'CKEditor: найдено {total} товаров с картинками в тексте')

        if total == 0:
            return

        pending: list[Product] = []
        processed = 0

        for product in queryset.iterator(chunk_size=500):
            self._check_stop()
            changed = False
            for field_name in CKEDITOR_FIELDS:
                original = getattr(product, field_name) or ''
                updated, count = apply_all_replacements(original, pairs)
                if count and updated != original:
                    setattr(product, field_name, updated)
                    changed = True

            processed += 1
            if changed:
                if self.options.dry_run:
                    self.stats.db_text_fields += 1
                else:
                    pending.append(product)

            if len(pending) >= BULK_BATCH_SIZE and not self.options.dry_run:
                Product.objects.bulk_update(pending, list(CKEDITOR_FIELDS), batch_size=BULK_BATCH_SIZE)
                self.stats.db_text_fields += len(pending)
                self._log(f'CKEditor: сохранено {self.stats.db_text_fields}/{total}...', 'db')
                pending = []
            elif processed % 1000 == 0:
                self._log(f'CKEditor: обработано {processed}/{total}...', 'db')

        if pending and not self.options.dry_run:
            Product.objects.bulk_update(pending, list(CKEDITOR_FIELDS), batch_size=BULK_BATCH_SIZE)
            self.stats.db_text_fields += len(pending)

        if self.stats.db_text_fields:
            self._log(f'CKEditor: итого {self.stats.db_text_fields} товаров обновлено', 'db')

    @staticmethod
    def _chunked(items: list[str], size: int):
        for index in range(0, len(items), size):
            yield items[index:index + size]

    def _clear_thumbnail_cache(self, media_root: Path):
        cache_dir = media_root / 'cache'
        if cache_dir.exists():
            for item in cache_dir.rglob('*'):
                if item.is_file():
                    item.unlink()
            self._log('Очищен media/cache/', 'info')

        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM thumbnail_kvstore')
        self._log('Очищена таблица thumbnail_kvstore (sorl-thumbnail)', 'info')

    def _print_summary(self):
        self._log('=' * 60)
        self._log('ИТОГ')
        self._log(f'Просмотрено файлов: {self.stats.scanned}')
        self._log(f'Конвертировано: {self.stats.converted}')
        self._log(f'Пропущено: {self.stats.skipped}')
        self._log(f'Ошибок: {self.stats.failed}')
        self._log(f'ImageField обновлено: {self.stats.db_image_fields}')
        self._log(f'CKEditor полей обновлено: {self.stats.db_text_fields}')
        self._log(f'Удалено оригиналов: {self.stats.deleted_originals}')
        self._log(f'Экономия: {format_size(self.stats.saved_bytes)}')
        if self.options.dry_run:
            self._log('DRY-RUN: изменения не применены.', 'warn')
        if self.stats.errors:
            self._log('Ошибки:', 'error')
            for error in self.stats.errors[:20]:
                self._log(f'  - {error}', 'error')


def execute_optimizer_job(options: OptimizerOptions, started_by: str) -> ConversionStats:
    """Запуск оптимизации в отдельном процессе (CLI или subprocess)."""
    manager = MediaOptimizerJobManager

    def log_callback(message: str, level: str = 'info'):
        manager.append_log(message, level)

    def stats_callback(stats: ConversionStats):
        state = manager._read_state_raw()
        if state.get('status') != 'running':
            return
        state['stats'] = asdict(stats)
        manager.write_state(state)

    def should_stop() -> bool:
        return manager.is_cancel_requested()

    try:
        manager.append_log(f'Запуск: {started_by} (pid {os.getpid()})')
        optimizer = MediaWebpOptimizer(
            options=options,
            log=log_callback,
            should_stop=should_stop,
            on_stats=stats_callback,
        )
        stats = optimizer.run()
        if manager.is_cancel_requested():
            raise JobCancelledError()

        manager.write_state({
            'status': 'done',
            'pid': os.getpid(),
            'started_at': manager._read_state_raw().get('started_at'),
            'finished_at': timezone.now().isoformat(),
            'started_by': started_by,
            'options': asdict(options),
            'stats': asdict(stats),
        })
        manager.clear_cancel()
        manager._write_report(options, stats)
        manager.append_log('Готово.', 'success')
        return stats
    except JobCancelledError:
        manager.append_log('Остановлено.', 'warn')
        state = manager._read_state_raw()
        state.update({
            'status': 'cancelled',
            'finished_at': timezone.now().isoformat(),
            'message': 'Остановлено пользователем.',
        })
        manager.write_state(state)
        manager.clear_cancel()
        return ConversionStats()
    except Exception as exc:
        manager.append_log(f'Критическая ошибка: {exc}', 'error')
        state = manager._read_state_raw()
        state.update({
            'status': 'error',
            'finished_at': timezone.now().isoformat(),
            'error': str(exc),
        })
        manager.write_state(state)
        manager.clear_cancel()
        raise


class MediaOptimizerJobManager:
    _lock = threading.RLock()

    @classmethod
    def workspace_dir(cls) -> Path:
        path = Path(settings.BASE_DIR) / 'logs' / 'media_optimizer'
        path.mkdir(parents=True, exist_ok=True)
        return path

    @classmethod
    def log_path(cls) -> Path:
        return cls.workspace_dir() / 'run.log'

    @classmethod
    def report_path(cls) -> Path:
        return cls.workspace_dir() / 'report.html'

    @classmethod
    def state_path(cls) -> Path:
        return cls.workspace_dir() / 'state.json'

    @classmethod
    def cancel_flag_path(cls) -> Path:
        return cls.workspace_dir() / 'cancel.flag'

    @classmethod
    def stderr_log_path(cls) -> Path:
        return cls.workspace_dir() / 'subprocess.stderr.log'

    @classmethod
    def _is_pid_alive(cls, pid: int | None) -> bool:
        if not pid:
            return False

        if os.name == 'posix':
            proc_status = Path(f'/proc/{pid}/status')
            if not proc_status.exists():
                return False
            try:
                content = proc_status.read_text(encoding='utf-8', errors='ignore')
            except OSError:
                return False
            for line in content.splitlines():
                if line.startswith('State:'):
                    proc_state = line.split()[1]
                    if proc_state == 'Z':
                        return False
                    return proc_state in {'R', 'S', 'D', 'I', 'W'}
            return False

        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True

    @classmethod
    def _append_process_diagnostics(cls, prefix: str = ''):
        stderr_path = cls.stderr_log_path()
        if not stderr_path.exists() or stderr_path.stat().st_size == 0:
            return
        tail = stderr_path.read_text(encoding='utf-8', errors='ignore').strip()[-4000:]
        if tail:
            cls.append_log(f'{prefix}Вывод stderr процесса:\n{tail}', 'error')

    @classmethod
    def _mark_process_failed(cls, message: str):
        cls.append_log(message, 'error')
        cls._append_process_diagnostics()
        state = cls._read_state_raw()
        if state.get('status') != 'running':
            return
        state.update({
            'status': 'error',
            'finished_at': timezone.now().isoformat(),
            'message': message,
        })
        cls.write_state(state)
        cls.clear_cancel()

    @classmethod
    def is_cancel_requested(cls) -> bool:
        return cls.cancel_flag_path().exists()

    @classmethod
    def clear_cancel(cls):
        flag = cls.cancel_flag_path()
        if flag.exists():
            flag.unlink()

    @classmethod
    def request_stop(cls):
        cls.cancel_flag_path().write_text('1', encoding='utf-8')

    @classmethod
    def sync_state(cls) -> dict:
        state = cls._read_state_raw()
        if state.get('status') != 'running':
            return state

        pid = state.get('pid')
        if cls._is_pid_alive(pid):
            return state

        cls._append_process_diagnostics('Процесс завершился неожиданно. ')
        state['status'] = 'stopped'
        state['finished_at'] = timezone.now().isoformat()
        state['message'] = (
            'Процесс завершился до окончания работы. '
            'Смотрите logs/media_optimizer/subprocess.stderr.log и строки [BOOT] в run.log.'
        )
        cls.write_state(state)
        cls.clear_cancel()
        return state

    @classmethod
    def force_reset(cls):
        with cls._lock:
            cls.clear_cancel()
            cls.log_path().write_text('', encoding='utf-8')
            cls.write_state({
                'status': 'idle',
                'message': 'Статус сброшен вручную.',
                'stats': asdict(ConversionStats()),
            })

    @classmethod
    def is_running(cls) -> bool:
        state = cls.sync_state()
        if state.get('status') != 'running':
            return False
        pid = state.get('pid')
        if pid is None:
            return True
        if cls.is_cancel_requested() and not cls._is_pid_alive(pid):
            return False
        return cls._is_pid_alive(pid)

    @classmethod
    def _read_state_raw(cls) -> dict:
        if not cls.state_path().exists():
            return {'status': 'idle'}
        try:
            return json.loads(cls.state_path().read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            return {'status': 'idle'}

    @classmethod
    def read_state(cls) -> dict:
        return cls.sync_state()

    @classmethod
    def write_state(cls, payload: dict):
        cls.state_path().write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )

    @classmethod
    def append_log(cls, message: str, level: str = 'info'):
        timestamp = timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')
        line = f'[{timestamp}] [{level.upper()}] {message}\n'
        with cls._lock:
            with cls.log_path().open('a', encoding='utf-8') as log_file:
                log_file.write(line)

    @classmethod
    def read_log(cls, from_line: int = 0) -> tuple[list[dict], int]:
        if not cls.log_path().exists():
            return [], 0

        lines = cls.log_path().read_text(encoding='utf-8').splitlines()
        total = len(lines)
        selected = lines[from_line:]
        entries = []
        for index, line in enumerate(selected, start=from_line):
            level = 'info'
            if '] [' in line:
                level_part = line.split('] [', 2)
                if len(level_part) >= 2:
                    level = level_part[1].rstrip(']').lower()
            entries.append({'line': index, 'text': line, 'level': level})
        return entries, total

    @classmethod
    def _build_subprocess_command(cls, options: OptimizerOptions) -> list[str]:
        launcher_py = str(Path(settings.BASE_DIR) / 'core' / 'media_optimizer_launcher.py')
        cmd = [
            sys.executable,
            '-u',
            launcher_py,
            '--quality', str(options.quality),
            '--max-width', str(options.max_width),
        ]
        if options.media_root:
            cmd.extend(['--media-root', options.media_root])
        if options.dry_run:
            cmd.append('--dry-run')
        if options.keep_originals:
            cmd.append('--keep-originals')
        if options.skip_db:
            cmd.append('--skip-db')
        if options.skip_files:
            cmd.append('--skip-files')
        return cmd

    @classmethod
    def start(cls, options: OptimizerOptions, started_by: str):
        with cls._lock:
            cls.sync_state()
            if cls.is_running():
                raise RuntimeError('Оптимизация уже выполняется.')

            cls.clear_cancel()
            cls.log_path().write_text('', encoding='utf-8')
            cls.write_state({
                'status': 'running',
                'pid': None,
                'started_at': timezone.now().isoformat(),
                'started_by': started_by,
                'options': asdict(options),
                'stats': asdict(ConversionStats()),
                'mode': 'subprocess',
            })

        cls.append_log('Подготовка к запуску...', 'info')
        command = cls._build_subprocess_command(options)
        stderr_path = cls.stderr_log_path()
        stderr_path.write_text('', encoding='utf-8')

        def _launch():
            stderr_handle = stderr_path.open('a', encoding='utf-8')
            exit_code = 0
            aborted = False
            try:
                process = subprocess.Popen(
                    command,
                    cwd=str(settings.BASE_DIR),
                    stdout=subprocess.DEVNULL,
                    stderr=stderr_handle,
                    start_new_session=True,
                )
                with cls._lock:
                    state = cls._read_state_raw()
                    if state.get('status') != 'running':
                        process.terminate()
                        aborted = True
                        return
                    state['pid'] = process.pid
                    cls.write_state(state)
                cls.append_log(
                    f'Задача запущена в отдельном процессе pid {process.pid}',
                    'info',
                )
                exit_code = process.wait()
            except Exception as exc:
                cls._mark_process_failed(f'Ошибка запуска процесса: {exc}')
                return
            finally:
                stderr_handle.close()

            if not aborted and exit_code != 0:
                cls._mark_process_failed(f'Процесс завершился с кодом {exit_code}')

        threading.Thread(target=_launch, daemon=True).start()

    @classmethod
    def stop(cls) -> bool:
        with cls._lock:
            state = cls.sync_state()
            if state.get('status') != 'running':
                return False
            cls.request_stop()
        cls.append_log('Запрошена остановка...', 'warn')
        return True

    @classmethod
    def _write_report(cls, options: OptimizerOptions, stats: ConversionStats):
        started_at = cls.read_state().get('started_at', '')
        finished_at = timezone.now().isoformat()
        log_lines = cls.log_path().read_text(encoding='utf-8') if cls.log_path().exists() else ''

        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Отчёт оптимизации media</title>
  <style>
    body {{ font-family: "Segoe UI", sans-serif; background:#f5f5f5; color:#1a1a18; margin:0; padding:24px; }}
    .wrap {{ max-width: 1100px; margin: 0 auto; }}
    h1 {{ margin: 0 0 8px; color:#00304e; }}
    .meta {{ color:#666; margin-bottom:24px; }}
    .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin-bottom:24px; }}
    .card {{ background:#fff; border-radius:12px; padding:16px; box-shadow:0 8px 24px rgba(0,0,0,.08); }}
    .card strong {{ display:block; font-size:28px; color:#3391c5; }}
    pre {{ background:#0f172a; color:#e2e8f0; padding:16px; border-radius:12px; overflow:auto; white-space:pre-wrap; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Отчёт оптимизации изображений</h1>
    <div class="meta">Старт: {started_at}<br>Финиш: {finished_at}<br>Режим: {"DRY-RUN" if options.dry_run else "ЗАПИСЬ"}</div>
    <div class="cards">
      <div class="card"><strong>{stats.scanned}</strong>Просмотрено</div>
      <div class="card"><strong>{stats.converted}</strong>Конвертировано</div>
      <div class="card"><strong>{stats.skipped}</strong>Пропущено</div>
      <div class="card"><strong>{stats.failed}</strong>Ошибок</div>
      <div class="card"><strong>{stats.db_image_fields}</strong>ImageField в БД</div>
      <div class="card"><strong>{stats.db_text_fields}</strong>CKEditor полей</div>
      <div class="card"><strong>{format_size(stats.saved_bytes)}</strong>Экономия</div>
    </div>
    <pre>{log_lines}</pre>
  </div>
</body>
</html>"""
        cls.report_path().write_text(html, encoding='utf-8')
