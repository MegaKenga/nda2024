from django.db import models

from pathlib import Path


class BaseFields(models.Model):
    name = models.CharField(default='', max_length=128)

    class Meta:
        abstract = True


class LogoImage(BaseFields):
    image = models.ImageField(
        upload_to='images/logo',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Логотипы'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        extension = Path(self.image.name).suffix[1:].lower()
        self.image.name = 'Logo ' + self.name + extension
        super(LogoImage, self).save(*args, **kwargs)


class BannerImage(BaseFields):
    image = models.ImageField(
        upload_to='images/banner',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        extension = Path(self.image.name).suffix[1:].lower()
        self.image.name = 'Banner ' + self.name + extension
        super(BannerImage, self).save(*args, **kwargs)


class RegistrationFile(BaseFields):
    category = models.ForeignKey(
        'catalog.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Регистрационное удостоверение',
        related_name='registration'
    )
    file = models.FileField(upload_to='files/registration', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Регистрационные удостоверения'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        extension = Path(self.file.name).suffix
        self.file.name = 'RU ' + self.name + extension
        super(RegistrationFile, self).save(*args, **kwargs)


class InstructionFile(BaseFields):
    category = models.ForeignKey(
        'catalog.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Инструкция',
        related_name='instruction'
    )
    file = models.FileField(upload_to='files/instruction', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Инструкции'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        extension = Path(self.file.name).suffix
        self.file.name = 'RU ' + self.name + extension
        super(InstructionFile, self).save(*args, **kwargs)


class OfferImage(BaseFields):
    offer = models.ForeignKey(
        'catalog.Offer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Изображение товара',
        related_name='offer_picture'
    )
    image = models.ImageField(
        upload_to='images/offer_pictures',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Изображения товара'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        extension = Path(self.image.name).suffix[1:].lower()
        self.image.name = 'Picture ' + self.name + extension
        super(OfferImage, self).save(*args, **kwargs)


class OfferTechDescription(BaseFields):
    offer = models.ForeignKey(
        'catalog.Offer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Техническое описание',
        related_name='tech_description'
    )
    file = models.FileField(
        upload_to='files/tech_description',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Технические описания'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        extension = Path(self.file.name).suffix[1:].lower()
        self.file.name = 'Tech description' + self.name + extension
        super(OfferTechDescription, self).save(*args, **kwargs)
