from django.db import models
from django.urls import reverse
from files.models import NDAImage

"""Общие классы и миксины"""


class NotHidden(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PUBLISHED')


class BaseFieldsMixin(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Черновик'
        PUBLISHED = 'PUBLISHED', 'Активен'
        ARCHIVED = 'ARCHIVED', 'В архиве'

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
    status = models.CharField(
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Статус показа на страницах'
    )
    slug = models.SlugField(default='None', max_length=128, db_index=True, verbose_name='url-адрес')

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        abstract = True


"""Модели"""


class Unit(BaseFieldsMixin):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Направление')
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Родительское направление')

    class Meta:
        ordering = ['place']
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def get_absolute_url(self):
        return reverse('unit', kwargs={'unit_slug': self.slug})

    def __str__(self):
        return self.name


class Brand(BaseFieldsMixin):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Бренд')

    class Meta:
        ordering = ['place']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def get_absolute_url(self):
        return reverse('brand', kwargs={'brand_slug': self.slug})

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
    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Направление, к которому относится категория'
    )
    is_final = models.BooleanField(default=False, verbose_name='Отметка о том, что категория является финальной и в ней содержатся товары')

    image = models.ForeignKey(NDAImage, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['place']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name


class Offer(BaseFieldsMixin):
    name = models.CharField(
        max_length=128,
        verbose_name='Артикул'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offer',
        verbose_name='Категория, к которой принадлежит товар'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
