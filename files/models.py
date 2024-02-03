from django.db import models

import os.path

from pathlib import Path


def get_upload_path(self, filename):
    if self.category_link is not None:
        return os.path.join('category', filename)
    return os.path.join('default', filename)


class ModelImage(models.Model):
    name = models.CharField(default='', max_length=50)
    file = models.ImageField(upload_to=get_upload_path, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Изображения'

    def save(self, *args, **kwargs):
        file_format = self.file
        extension = Path(file_format.name).suffix[1:].lower()
        file_name = self.name + "." + extension
        self.file.name = file_name
        super(ModelImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.name