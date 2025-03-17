from django.db import models
from django.utils.safestring import mark_safe
import os
from catalog.models import Product

class ModelImage(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Продукт')
    image = models.ImageField(upload_to='product/images', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Изображения'
        verbose_name = 'Изображение'

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{0}" width="150" height="150" />'.format(self.image.url))
        else:
            return '(No image)'
    
    def __str__(self):
        if self.image:
            return self.image.url
        return '(No image)'
    
    def get_filename(self):
        return os.path.basename(self.file.name)

class ModelFile(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Продукт')
    file = models.FileField(upload_to='product/certificates', null=True, blank=True, verbose_name='Файл')

    class Meta:
        verbose_name_plural = 'РУ и Сертификаты'
        verbose_name = 'РУ и Сертификат'

    def __str__(self):
        if self.file:
            return self.file.url
        return '(No file)'
    
    def get_filename(self):
        return os.path.basename(self.file.name)
    

class InstructionsFile(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Продукт')
    file = models.FileField(upload_to='product/instructions', null=True, blank=True, verbose_name='Файл')

    class Meta:
        verbose_name_plural = 'Инструкции'
        verbose_name = 'Инструкция'

    def __str__(self):
        if self.file:
             return self.file.url
        return '(No file)'
    
    def get_filename(self):
           return os.path.basename(self.file.name)
    
class CatalogFile(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Продукт')
    file = models.FileField(upload_to='product/catalog', null=True, blank=True, verbose_name='Файл')

    class Meta:
        verbose_name_plural = 'Каталог'
        verbose_name = 'Файл каталога'

    def __str__(self):
       if self.file:
           return self.file.url
       return '(No file)'
    
    def get_filename(self):
        return os.path.basename(self.file.name)

