from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Brand, Category, Product, Offer


def update_related_models_status(instance, related_model, field_name, status):
    """Вспомогательная функция для обновления статуса связанных моделей"""
    filter_kwargs = {field_name: instance}
    related_model.objects.filter(**filter_kwargs).update(status=status)


# Указываем конкретные модели-отправители
@receiver(pre_save, sender=Brand)
@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Product)
def cascade_status_update(sender, instance, **kwargs):
    """Универсальный обработчик для каскадного обновления статуса"""
    # Проверяем, что модель наследуется от BaseFields
    if not hasattr(instance, 'status'):
        return

    if not instance.pk:
        return

    # Получаем старую модель из базы данных
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    # Если статус не изменился, выходим
    if old_instance.status == instance.status:
        return

    # Определяем связи между моделями
    relation_map = {
        Brand: [
            (Category, 'brand'),
            (Product, 'brand'),
            (Offer, 'product__brand'),
        ],
        Category: [
            (Product, 'parents'),
            (Offer, 'product__parents'),
        ],
        Product: [
            (Offer, 'product'),
        ],
    }

    # Обновляем связанные модели
    if sender in relation_map:
        for model_class, field_name in relation_map[sender]:
            try:
                update_related_models_status(instance, model_class, field_name, instance.status)
            except Exception as e:
                # Логируем ошибку, но продолжаем выполнение
                print(f"Error updating {model_class.__name__}: {e}")
