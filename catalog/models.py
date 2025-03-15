from django.db import models
from django.urls import reverse
from django.core.cache import cache
from django_ckeditor_5.fields import CKEditor5Field


"""Общие классы и миксины"""


class NotHidden(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PUBLISHED')


class BaseFields(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Черновик'
        PUBLISHED = 'PUBLISHED', 'Активен'
        ARCHIVED = 'ARCHIVED', 'В архиве'

    place = models.IntegerField(
        blank=True,
        null=True,
        default=0,  # Добавлено значение по умолчанию
        verbose_name='Место в списке'
    )
    status = models.CharField(
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Статус показа на страницах'
    )
    title = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='Title'
    )
    ceo_description = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='CEO Description'
    )
    keywords = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='Keywords'
    )

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        abstract = True


"""Модели"""


class Specialist(models.Model):
    name = models.CharField(max_length=56, verbose_name='Имя специалиста')
    phone = models.CharField(max_length=28, verbose_name='Телефон')
    email = models.EmailField(max_length=56, verbose_name='Email')

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        cache_key = f'specialist_{self.pk}'
        cache.delete(cache_key)  # Инвалидируем кэш
        super().save(*args, **kwargs)  # Сохраняем объект

    def delete(self, *args, **kwargs):
        cache_key = f'specialist_{self.pk}'
        cache.delete(cache_key)  # Инвалидируем кэш
        super().delete(*args, **kwargs)  # Удаляем объект


class Brand(BaseFields):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Бренд')
    description = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='Описание бренда'

    )
    logo = models.ImageField(
        upload_to='brand/logo',
        default='',
        blank=True,
        verbose_name='Логотип бренда'
    )
    banner_color = models.CharField(
        max_length=32,
        default='#3391c5',
        null=True,
        verbose_name='Цвет баннера бренда'
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

    def save(self, *args, **kwargs):
        cache_key_breadcrumbs = f'brand_breadcrumbs {self.slug}'
        cache.delete(cache_key_breadcrumbs)
        super().save(*args, **kwargs)  # Сначала сохраняем, потом инвалидируем кэш

    def delete(self, *args, **kwargs):
        cache_key_breadcrumbs = f'brand_breadcrumbs {self.slug}'
        cache.delete(cache_key_breadcrumbs)
        super().delete(*args, **kwargs)  # Сначала удаляем, потом инвалидируем кэш


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
    logo = models.ImageField(
        upload_to='category/logo',
        default='',
        null=True,
        blank=True,
        verbose_name='Логотип'
    )
    slug = models.SlugField(
        unique=True,
        max_length=128,
        db_index=True,
        verbose_name='url-адрес'
    )
    banner_color = models.CharField(
        max_length=32,
        default='',
        null=True,
        verbose_name='Цвет баннера категории'
    )

    @property
    def colour(self):
        if not self.brand:
            self.banner_color = '#3391c5'
        self.banner_color = self.brand.banner_color
        return self.banner_color

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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
    

class Product(BaseFields):
    name = models.CharField(
        max_length=256,
        verbose_name='Название товара'
    )
    logo = models.ImageField(
        upload_to='product/logo',
        default='',
        null=True,
        blank=True,
        verbose_name='Логотип'
    )
    parents = models.ManyToManyField(
        'Category',
        blank=True,
        verbose_name='Родительские категории',
        related_name='children',
        symmetrical=False
    )
    short_description = CKEditor5Field(
        default='',
        null=True,
        blank=True,
        verbose_name='Краткое описание',
        config_name='default'  # Используем конфигурацию по умолчанию
    )
    full_description = CKEditor5Field(
        default='',
        null=True,
        blank=True,
        verbose_name='Полное описание',
        config_name='default'
    )
    characteristics = CKEditor5Field(
        default='',
        null=True,
        blank=True,
        verbose_name='Характеристики',
        config_name='default'
    )
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Специалист, ответственный за категорию'
    )
    youtube_link = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Ссылка на YouTube'
    )
    rutube_link = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Ссылка Rutube'
    )
    slug = models.SlugField(
        unique=True,
        max_length=128,
        db_index=True,
        verbose_name='url-адрес'
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})


class Offer(BaseFields):
    name = models.CharField(
        max_length=128,
        verbose_name='Артикул'
    )
    text_description = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='Краткое описание (текст)',
    )
    shipping_pack = models.CharField(
        max_length=10,
        verbose_name="Количество в упаковке",
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offer',
        verbose_name='Товар, к которому принадлежит код'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Код'
        verbose_name_plural = 'Коды'

    def __str__(self): # __str__
        return self.name

    def save(self, *args, **kwargs):
        # Инвалидируем кэш, связанный с этим Offer
        cache_key_offer = f'offer_{self.pk}'
        cache.delete(cache_key_offer)

        # Также инвалидируем кэш, связанный с категорией этого Offer
        if self.product:
            cache_key_category = f'category_{self.product.slug}'
            cache.delete(cache_key_category)

        super().save(*args, **kwargs)  # Сначала сохраняем, потом инвалидируем кэш

    def delete(self, *args, **kwargs):
        # Инвалидируем кэш, связанный с этим Offer
        cache_key_offer = f'offer_{self.pk}'
        cache.delete(cache_key_offer)

        # Также инвалидируем кэш, связанный с категорией этого Offer
        if self.product:
            cache_key_category = f'category_{self.product.slug}'
            cache.delete(cache_key_category)

        super().delete(*args, **kwargs)  # Сначала удаляем, потом инвалидируем кэш
