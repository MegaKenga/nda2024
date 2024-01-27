from django.db import models

from pathlib import Path


class ModelImage(models.Model):
    name = models.CharField(default='', max_length=50)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        file_format = self.image
        extension = Path(file_format.name).suffix[1:].lower()
        file_name = self.name + "." + extension
        self.image.name = file_name
        super(ModelImage, self).save(*args, **kwargs)


class ModelFile(models.Model):
    name = models.CharField(default='', max_length=50)
    file = models.FileField(upload_to='files', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        file_format = self.file
        extension = Path(file_format.name).suffix
        file_name = self.name + extension
        self.file.name = file_name
        super(ModelFile, self).save(*args, **kwargs)
