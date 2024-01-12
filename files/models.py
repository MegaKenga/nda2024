from os import path

from django.db import models

from nda import settings


class CatalogImage(models.Model):
    name = models.CharField(default='', max_length=50)
    image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        file_name = self.name + '.jpeg'
        self.image.name = file_name
        super(CatalogImage, self).save(*args, **kwargs)
