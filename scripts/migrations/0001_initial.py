# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Например: Google Analytics, Яндекс.Метрика, Facebook Pixel', max_length=200, verbose_name='Название скрипта')),
                ('description', models.TextField(blank=True, help_text='Краткое описание назначения скрипта', verbose_name='Описание')),
                ('code', models.TextField(help_text='HTML/JavaScript код для вставки', verbose_name='Код скрипта')),
                ('position', models.CharField(choices=[('head', 'В <head>'), ('body_start', 'После открытия <body>'), ('body_end', 'Перед закрытием </body>'), ('footer', 'В footer')], default='head', max_length=20, verbose_name='Позиция размещения')),
                ('is_active', models.BooleanField(default=True, help_text='Включить/выключить скрипт', verbose_name='Активен')),
                ('order', models.PositiveIntegerField(default=0, help_text='Порядок загрузки скриптов (меньше число = раньше загружается)', verbose_name='Порядок')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Скрипт',
                'verbose_name_plural': 'Скрипты',
                'ordering': ['position', 'order', 'name'],
            },
        ),
    ]