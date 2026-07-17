from __future__ import annotations

from dataclasses import asdict

from django.conf import settings
from django.core.management.base import BaseCommand

from core.media_webp_optimizer import (
    MediaOptimizerJobManager,
    OptimizerOptions,
    execute_optimizer_job,
)


class Command(BaseCommand):
    help = 'Сжимает и конвертирует изображения media/ в WebP, обновляет пути в PostgreSQL.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--media-root',
            default='',
            help='Путь к media (по умолчанию settings.MEDIA_ROOT).',
        )
        parser.add_argument('--quality', type=int, default=82)
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--keep-originals', action='store_true')
        parser.add_argument('--skip-db', action='store_true')
        parser.add_argument('--skip-files', action='store_true')
        parser.add_argument(
            '--managed-job',
            action='store_true',
            help='Запуск из веб-интерфейса: пишет лог в logs/media_optimizer/.',
        )

    def handle(self, *args, **options):
        optimizer_options = OptimizerOptions(
            media_root=options['media_root'],
            quality=options['quality'],
            dry_run=options['dry_run'],
            keep_originals=options['keep_originals'],
            skip_db=options['skip_db'],
            skip_files=options['skip_files'],
        )

        if options['managed_job']:
            state = MediaOptimizerJobManager._read_state_raw()
            started_by = state.get('started_by', 'managed-job')
            execute_optimizer_job(optimizer_options, started_by)
            return

        from core.media_webp_optimizer import MediaWebpOptimizer

        optimizer = MediaWebpOptimizer(
            options=optimizer_options,
            log=self._log,
        )
        optimizer.run()

    def _log(self, message: str, level: str = 'info'):
        if level == 'error':
            self.stderr.write(self.style.ERROR(message))
        elif level in ('success', 'warn'):
            self.stdout.write(self.style.WARNING(message))
        else:
            self.stdout.write(message)
