from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class NotHidden(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class DataModelsMixin(models.Model):
    description = models.TextField(default='', verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активная категория')

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        abstract = True


class Brand(DataModelsMixin):
    name = models.CharField(max_length=256, unique=True, verbose_name='Бренд')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Category(DataModelsMixin, MPTTModel):
    name = models.CharField(max_length=512, verbose_name='Категория')
    parent = TreeForeignKey(
        'self',
        related_name='children',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='ID родительской категории'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(DataModelsMixin):
    name = models.CharField(max_length=512, unique=True, verbose_name='Товар')
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='ID бренда, к которому относится товар'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='ID категории, к которой относится товар'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
