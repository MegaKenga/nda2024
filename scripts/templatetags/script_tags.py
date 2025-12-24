from django import template
from django.utils.safestring import mark_safe
from ..models import Script

register = template.Library()


@register.simple_tag
def render_scripts(position):
    """
    Рендерит скрипты для указанной позиции
    Использование: {% render_scripts 'head' %}
    """
    scripts = Script.objects.filter(
        is_active=True, 
        position=position
    ).order_by('order', 'name')
    
    output = []
    for script in scripts:
        output.append(f'<!-- {script.name} -->')
        output.append(script.code)
        output.append('')
    
    return mark_safe('\n'.join(output))


@register.inclusion_tag('scripts/script_block.html')
def script_block(position):
    """
    Включает шаблон с блоком скриптов
    Использование: {% script_block 'head' %}
    """
    scripts = Script.objects.filter(
        is_active=True, 
        position=position
    ).order_by('order', 'name')
    
    return {'scripts': scripts}