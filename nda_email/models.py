from django.db import models


class OrderNumber(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Текущий номер заказа')
    value = models.IntegerField(null=True, blank=True, verbose_name='Значение')

    class Meta:
        verbose_name = 'Номер заказа'
        verbose_name_plural = 'Номера заказов'

    def __str__(self):
        return self.name
