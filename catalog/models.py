from django.db import models
from django.urls import reverse
from django.db.models import Q

from files.models import ModelImage, ModelFile


"""Общие классы и миксины"""


class NotHidden(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PUBLISHED')


class BaseFields(models.Model):
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

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        abstract = True


"""Модели"""


class Brand(BaseFields):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Бренд')
    logo = models.ForeignKey(
        ModelImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Логотип бренда',
        related_name='brand_logo'
    )
    banner = models.ForeignKey(
        ModelImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Баннер бренда',
        related_name='brand_banner'
    )
    slug = models.SlugField(
        unique=True,
        max_length=128,
        db_index=True,
        verbose_name='url-адрес'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def get_absolute_url(self):
        return reverse('brand', kwargs={'brand_slug': self.slug})

    def __str__(self):
        return self.name.upper()


class Category(BaseFields):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Бренд, к которому относится категория'
    )
    parents = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name='Родительские категории',
        related_name='children',
        symmetrical=False
    )
    logo = models.ForeignKey(
        ModelImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Логотип категории',
        related_name='category_logo'
    )
    banner = models.ForeignKey(
        ModelImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Баннер категории',
        related_name='category_banner'
    )
    images = models.ManyToManyField(ModelImage, related_name='category', through="CategoryImage")
    certificate = models.ForeignKey(
        ModelFile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Регистрационное удостоверение',
        related_name='registration'
    )
    instruction = models.ForeignKey(
        ModelFile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Инструкция',
        related_name='instruction'
    )
    slug = models.SlugField(
        unique=True,
        max_length=128,
        db_index=True,
        verbose_name='url-адрес'
    )
    is_final = models.BooleanField(
        default=False,
        verbose_name='Отметка о том, что категория является финальной и в ней содержатся товары'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __str__(self):
        if self.brand:
            return str(self.brand).upper() + '----' + self.name.upper()
        return 'ПОДБОРКА' + '----' + self.name.upper()


class CategoryImage(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=False, blank=False,
        related_name='image_link',
        verbose_name='Image category'
    )
    file = models.ForeignKey(
        ModelImage,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='category_link',
        verbose_name='Category image'
    )


class Offer(BaseFields):
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
    tech_info = models.ForeignKey(
        ModelFile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Техзадание',
        related_name='tech_description'
    )
    ctru = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name='КТРУ'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
