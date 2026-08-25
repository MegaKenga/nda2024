import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps

# Замените на ваши модели и поля, где хранятся файлы
# Формат: ('app_label.ModelName', 'field_name')
MEDIA_FIELDS = [
    ('catalog.Brand', 'logo'),
    ('catalog.Category', 'logo'),
    ('catalog.Product', 'logo'),
    ('files.ModelImage', 'image'),
    ('files.ModelFile', 'file'),
    ('files.InstructionsFile', 'file'),
    ('files.CatalogFile', 'file'),
]


class Command(BaseCommand):
    help = 'Удаляет медиафайлы, которых нет в базе данных'

    def add_arguments(self, parser):
        # Добавляем флаг для безопасного запуска без удаления
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Проверить и показать файлы без фактического удаления',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        media_root = os.path.normpath(settings.MEDIA_ROOT)

        if dry_run:
            self.stdout.write(self.style.WARNING("=== РЕЖИМ ТЕСТИРОВАНИЯ (DRY RUN) ==="))

        self.stdout.write("Сбор относительных путей из базы данных...")
        valid_relative_paths = set()

        # Сбор путей из всех указанных моделей
        for model_path, field_name in MEDIA_FIELDS:
            try:
                model = apps.get_model(model_path)
                # Выбираем только непустые значения и убираем дубликаты на уровне БД
                queryset = model.objects.exclude(**{f"{field_name}": ""}).values_list(field_name, flat=True)

                for rel_path in queryset:
                    if rel_path:
                        # Нормализуем относительный путь (исправляет слеши)
                        valid_relative_paths.add(os.path.normpath(rel_path))
            except LookupError:
                self.stdout.write(self.style.ERROR(f"Модель {model_path} не найдена."))
                return

        self.stdout.write(f"Найдено {len(valid_relative_paths)} уникальных файлов в БД.")
        self.stdout.write("Сканирование папки MEDIA_ROOT...")

        deleted_files = 0
        deleted_dirs = 0

        # Обходим MEDIA_ROOT снизу вверх, чтобы безопасно удалять пустые папки
        for root, dirs, files in os.walk(media_root, topdown=False):
            for file in files:
                abs_file_path = os.path.join(root, file)

                # Получаем относительный путь файла относительно MEDIA_ROOT
                rel_file_path = os.path.relpath(abs_file_path, media_root)
                normalized_rel_path = os.path.normpath(rel_file_path)

                # Проверяем, есть ли относительный путь в нашем множестве из БД
                if normalized_rel_path not in valid_relative_paths:
                    if dry_run:
                        self.stdout.write(f"[Dry-run] Будет удален файл: {normalized_rel_path}")
                        deleted_files += 1
                    else:
                        try:
                            os.remove(abs_file_path)
                            self.stdout.write(self.style.SUCCESS(f"Удален файл: {normalized_rel_path}"))
                            deleted_files += 1
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Ошибка удаления {normalized_rel_path}: {e}"))

            # Удаление пустых директорий
            for d in dirs:
                abs_dir_path = os.path.join(root, d)
                try:
                    if not os.listdir(abs_dir_path):
                        if dry_run:
                            self.stdout.write(f"[Dry-run] Будет удалена пустая папка: {abs_dir_path}")
                            deleted_dirs += 1
                        else:
                            os.rmdir(abs_dir_path)
                            self.stdout.write(self.style.SUCCESS(f"Удалена пустая папка: {abs_dir_path}"))
                            deleted_dirs += 1
                except Exception:
                    pass

        self.stdout.write(self.style.SUCCESS(f"\nГотово! Обработано файлов: {deleted_files}, папок: {deleted_dirs}"))
