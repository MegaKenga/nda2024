# Generated by Django 4.2.7 on 2024-05-04 15:55

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Описание')),
                ('place', models.IntegerField(blank=True, null=True, verbose_name='Место в списке')),
                ('status', models.CharField(choices=[('DRAFT', 'Черновик'), ('PUBLISHED', 'Активен'), ('ARCHIVED', 'В архиве')], default='DRAFT', verbose_name='Статус показа на страницах')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Бренд')),
                ('logo', models.ImageField(blank=True, default='', upload_to='brand/logo', verbose_name='Логотип бренда')),
                ('banner', models.ImageField(blank=True, default='', upload_to='brand/banner', verbose_name='Баннер бренда')),
                ('slug', models.SlugField(max_length=128, unique=True, verbose_name='url-адрес')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
                'ordering': ['place'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Описание')),
                ('place', models.IntegerField(blank=True, null=True, verbose_name='Место в списке')),
                ('status', models.CharField(choices=[('DRAFT', 'Черновик'), ('PUBLISHED', 'Активен'), ('ARCHIVED', 'В архиве')], default='DRAFT', verbose_name='Статус показа на страницах')),
                ('name', models.CharField(max_length=256, verbose_name='Название категории')),
                ('logo', models.ImageField(blank=True, default='', null=True, upload_to='category/logo', verbose_name='Логотип категории')),
                ('banner', models.ImageField(blank=True, default='', upload_to='category/banner', verbose_name='Баннер категории')),
                ('instruction', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/files', location='/home/mega-kenga/PycharmProjects/collabtraining/trainingdjango/private/'), upload_to='instructions', verbose_name='Инструкция')),
                ('slug', models.SlugField(max_length=128, unique=True, verbose_name='url-адрес')),
                ('is_final', models.BooleanField(default=False, verbose_name='Отметка о том, что категория является финальной и в ней содержатся товары')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.brand', verbose_name='Бренд, к которому относится категория')),
                ('parents', models.ManyToManyField(blank=True, related_name='children', to='catalog.category', verbose_name='Родительские категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['place'],
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Описание')),
                ('place', models.IntegerField(blank=True, null=True, verbose_name='Место в списке')),
                ('status', models.CharField(choices=[('DRAFT', 'Черновик'), ('PUBLISHED', 'Активен'), ('ARCHIVED', 'В архиве')], default='DRAFT', verbose_name='Статус показа на страницах')),
                ('name', models.CharField(max_length=128, verbose_name='Артикул')),
                ('tech_info', models.FileField(blank=True, null=True, upload_to='files/instructions', verbose_name='Техзадание')),
                ('ctru', models.CharField(blank=True, max_length=64, null=True, verbose_name='КТРУ')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer', to='catalog.category', verbose_name='Категория, к которой принадлежит товар')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['place'],
            },
        ),
    ]
