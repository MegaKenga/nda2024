from django.db import models
from django.urls import reverse
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
    slug = models.SlugField(
        unique=True,
        max_length=128,
        db_index=True,
        null=True,
        blank=True,
        verbose_name='url-адрес'
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


class Brand(BaseFields):
    name = models.CharField(
        max_length=128,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Бренд',
    )
    description = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='Описание бренда'
    )
    logo = models.ImageField(
        upload_to='brand/logo',
        default='',
        null=True,
        blank=True,
        verbose_name='Логотип бренда'
    )
    banner_color = models.CharField(
        max_length=32,
        default='#3391c5',
        null=True,
        verbose_name='Цвет баннера бренда'
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
    name = models.TextField(
        default='',
        null=True,
        blank=True,
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
    name = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='Название товара'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Бренд, к которому относится товар'
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
        related_name='children_products',
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


    class Meta:
        ordering = ['place']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    def __str__(self):
        return str(self.brand).upper() + '----' + self.name.upper()


class Offer(models.Model):
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
    name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
        verbose_name="Количество в упаковке",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offer',
        verbose_name='Товар, к которому принадлежит код'
    )

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        ordering = ['place']
        verbose_name = 'Код'
        verbose_name_plural = 'Коды'

    def __str__(self): # __str__
        return self.name
