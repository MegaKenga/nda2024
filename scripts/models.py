from django.db import models


class ScriptPosition(models.TextChoices):
    HEAD = 'head', 'В <head>'
    BODY_START = 'body_start', 'После открытия <body>'
    BODY_END = 'body_end', 'Перед закрытием </body>'
    FOOTER = 'footer', 'В footer'


class Script(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название скрипта',
        help_text='Например: Google Analytics, Яндекс.Метрика, Facebook Pixel'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Краткое описание назначения скрипта'
    )
    
    code = models.TextField(
        verbose_name='Код скрипта',
        help_text='HTML/JavaScript код для вставки'
    )
    
    position = models.CharField(
        max_length=20,
        choices=ScriptPosition.choices,
        default=ScriptPosition.HEAD,
        verbose_name='Позиция размещения'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Включить/выключить скрипт'
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
        help_text='Порядок загрузки скриптов (меньше число = раньше загружается)'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Скрипт'
        verbose_name_plural = 'Скрипты'
        ordering = ['position', 'order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_position_display()})"