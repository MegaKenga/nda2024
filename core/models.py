from django.db import models
from catalog.models import Product, NotHidden


class MainPageInfoBlock(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Черновик'
        PUBLISHED = 'PUBLISHED', 'Активен'
        ARCHIVED = 'ARCHIVED', 'В архиве'

    block_name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name='Название рекламного блока | Служебная информация',
        default='',
    )
    block_header = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name='Заголовок рекламного блока | Отображается на странице',
        default='',
    )
    block_category = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Товар для рекламы на главной странице'
    )
    block_text = models.TextField(
        default= '''<li class="hero__list-item t-25">Особенность 1</li>
                    <li class="hero__list-item t-25">Особенность 2</li>
                    ''',
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    block_image = models.ImageField(
        upload_to='main_page/infoblock',
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

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        verbose_name = 'Реклама на главной странице'
        verbose_name_plural = 'Реклама на главной странице'

    def __str__(self):
        return self.block_name
