from django.db import models


"""Общие классы и миксины"""


class BaseFieldsMixin(models.Model):
    description = models.TextField(default='', verbose_name='Описание')
    place = models.IntegerField(blank=True, null=True, verbose_name='Место в списке')
    is_active = models.BooleanField(default=True, verbose_name='Статус показа на страницах')

    class Meta:
        abstract = True


"""Модели"""


class Brand(BaseFieldsMixin):
    name = models.CharField(max_length=128, unique=True, verbose_name='Бренд')

    class Meta:
        ordering = ['place']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Category(BaseFieldsMixin):
    name = models.CharField(max_length=128, unique=True, verbose_name='Название категории')
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Бренд, к которому относится категория'
    )
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Родительская категория'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(BaseFieldsMixin):
    name = models.CharField(max_length=128, unique=True, verbose_name='Название группы товаров')
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Бренд, к которому относится группа товаров'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='products',
        verbose_name='Категории, к которым принадлежит группа товаров'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Группа товара'
        verbose_name_plural = 'Группы товаров'

    def __str__(self):
        return self.name


class Offer(BaseFieldsMixin):
    name = models.CharField(max_length=128, unique=True, verbose_name='Артикул')
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Бренд, к которому относится товар'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='product',
        verbose_name='Группа, к которой принадлежит товар'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
