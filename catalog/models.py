from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=4000, verbose_name='Бренд')
    description = models.TextField(max_length=4000, blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=4000, verbose_name='Товар')
    description = models.TextField(max_length=4000, blank=True, null=True, verbose_name='Описание')
    brand_id = models.ForeignKey('Brand', on_delete=models.CASCADE, verbose_name='ID бренда, к которому относится товар')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=4000, verbose_name='Категория')
    parent_id = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, verbose_name='ID родительской категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='ID товара')
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='ID категории')

    class Meta:
        verbose_name = 'Связь товара и категории'
        verbose_name_plural = 'Связь товаров и категорий'

    def __str__(self):
        return self.product_id
