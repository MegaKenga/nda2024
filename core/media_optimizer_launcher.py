"""Точка входа для оптимизатора из веб-интерфейса (лог до загрузки Django)."""
from __future__ import annotations

import argparse
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'logs' / 'media_optimizer'
RUN_LOG = LOG_DIR / 'run.log'


def boot_log(message: str, level: str = 'BOOT') -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{timestamp}] [{level}] {message}\n'
    with RUN_LOG.open('a', encoding='utf-8') as log_file:
        log_file.write(line)


def main() -> int:
    parser = argparse.ArgumentParser(description='Media WebP optimizer worker')
    parser.add_argument('--media-root', default='')
    parser.add_argument('--quality', type=int, default=82)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--keep-originals', action='store_true')
    parser.add_argument('--skip-db', action='store_true')
    parser.add_argument('--skip-files', action='store_true')
    args = parser.parse_args()

    boot_log(f'Worker pid={os.getpid()}')
    os.chdir(BASE_DIR)
    sys.path.insert(0, str(BASE_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nda.settings')

    boot_log('Загрузка Django...')
    import django

    django.setup()
    boot_log('Django загружен, старт оптимизации...')

    from core.media_webp_optimizer import (
        MediaOptimizerJobManager,
        OptimizerOptions,
        execute_optimizer_job,
    )

    options = OptimizerOptions(
        media_root=args.media_root,
        quality=args.quality,
        dry_run=args.dry_run,
        keep_originals=args.keep_originals,
        skip_db=args.skip_db,
        skip_files=args.skip_files,
    )
    started_by = MediaOptimizerJobManager._read_state_raw().get('started_by', 'web-worker')
    execute_optimizer_job(options, started_by)
    boot_log('Worker завершён', 'BOOT')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        boot_log(f'FATAL: {exc}', 'ERROR')
        boot_log(traceback.format_exc(), 'ERROR')
        raise SystemExit(1) from exc
