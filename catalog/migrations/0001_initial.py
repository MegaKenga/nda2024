# Generated by Django 4.2.7 on 2023-12-08 19:08

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
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Бренд')),
                ('description', models.TextField(default='', verbose_name='Описание')),
                ('hide', models.BooleanField(default=False, verbose_name='Скрыть')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Категория')),
                ('hide', models.BooleanField(default=False, verbose_name='Скрыть')),
                ('parent', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='catalog.category', verbose_name='ID родительской категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True, verbose_name='Товар')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Описание')),
                ('hide', models.BooleanField(default=False, verbose_name='Скрыть')),
                ('brand', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='catalog.brand', verbose_name='ID бренда, к которому относится товар')),
                ('category', models.ManyToManyField(to='catalog.category', verbose_name='ID категории, к которой относится товар')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]
