from django.db import models
from catalog.models import Category


class MainPage(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Черновик'
        PUBLISHED = 'PUBLISHED', 'Активен'
        ARCHIVED = 'ARCHIVED', 'В архиве'

    advert_name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name='Название рекламного блока'
    )
    advert_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория для рекламы на главной странице'
    )
    advert_text = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        verbose_name='Текст рекламного блока'
    )
    advert_image = models.ImageField(
        upload_to='main_page/banner',
        default='',
        null=False,
        blank=False,
        verbose_name='Изображение для рекламного блока'
    )
    status = models.CharField(
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Статус показа на страницах'
    )

    class Meta:
        verbose_name = 'Реклама на главной странице'
        verbose_name_plural = 'Реклама на главной странице'

    def __str__(self):
        return self.advert_name
