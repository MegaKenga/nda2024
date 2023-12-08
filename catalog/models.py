from django.db import models
from django.urls import reverse


# Create your models here.


class NotHidden(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(hide=False)


class Brand(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name='Бренд')
    description = models.TextField(default='', verbose_name='Описание')
    hide = models.BooleanField(default=False, verbose_name='Скрыть')

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=512, unique=True, verbose_name='Товар')
    description = models.TextField(default='', null=True, blank=True, verbose_name='Описание')
    brand = models.ForeignKey(Brand, default='', on_delete=models.SET_DEFAULT, verbose_name='ID бренда, к которому относится товар')
    category = models.ManyToManyField('Category', verbose_name='ID категории, к которой относится товар')
    hide = models.BooleanField(default=False, verbose_name='Скрыть')

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=512, verbose_name='Категория')
    parent = models.ForeignKey('self', default='', on_delete=models.SET_DEFAULT, null=True, blank=True, verbose_name='ID родительской категории')
    hide = models.BooleanField(default=False, verbose_name='Скрыть')

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
