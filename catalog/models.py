from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


"""Общие классы и миксины"""
class NotHidden(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class DataModelsMixin(models.Model):
    description = models.TextField(default='', verbose_name='Описание')
    place = models.IntegerField(blank=True, null=True, verbose_name='Место в списке')
    is_active = models.BooleanField(default=True, verbose_name='Активная категория')

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        abstract = True


"""Модели"""
class Brand(DataModelsMixin):
    name = models.CharField(max_length=128, verbose_name='Бренд')
    # image = models.ImageField(upload_to='catalog/images/image', blank=True, null=True, verbose_name='Изображение')
    # banner = models.ImageField(upload_to='catalog/images/banner', blank=True, null=True, verbose_name='Баннер')

    class Meta:
        ordering = ['place']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Category(DataModelsMixin, MPTTModel):
    name = models.CharField(max_length=128, verbose_name='Имя группы')
    brand = models.ForeignKey(
        Brand,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='ID Бренда, к которому относится группа'
    )
    parent = TreeForeignKey(
        'self',
        related_name='children',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='ID родительской категории'
    )
    # image = models.ImageField(upload_to='catalog/images/image', blank=True, null=True, verbose_name='Изображение')
    # banner = models.ImageField(upload_to='catalog/images/banner', blank=True, null=True, verbose_name='Баннер')

    class Meta:
        ordering = ['place']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(DataModelsMixin):
    name = models.CharField(max_length=50, unique=True, verbose_name='Товар')
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='ID бренда, к которому относится товар'
    )
    category = models.ForeignKey(
        'Category',
        null=True,
        related_name='ancestor_for_product',
        on_delete=models.SET_NULL,
        verbose_name='Уникальный ID группы, к которой принадлежит товар'
    )
    # image = models.ImageField(upload_to='catalog/images/image', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        ordering = ['place']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
