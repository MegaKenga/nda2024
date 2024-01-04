from django.db import models


"""Общие классы и миксины"""


class NotHidden(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BaseFieldsMixin(models.Model):
    description = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    place = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Место в списке'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Статус показа на страницах'
    )

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        abstract = True


"""Модели"""


class Brand(BaseFieldsMixin):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Бренд')

    class Meta:
        ordering = ['place']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Category(BaseFieldsMixin):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Название категории'
    )
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
        if self.parent is not None:
            return self.name + " <" + self.parent.name + ">"
        return self.name


class ProductGroup(BaseFieldsMixin):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Название группы товаров')
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
    name = models.CharField(
        max_length=128,
        verbose_name='Артикул'
    )
    product_group = models.ForeignKey(
        ProductGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='product',
        verbose_name='Группа, к которой принадлежит товар'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
