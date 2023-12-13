from django.db import models


class NotHidden(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class DataModelsMixin(models.Model):
    description = models.TextField(default='', verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активная категория')

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        abstract = True
