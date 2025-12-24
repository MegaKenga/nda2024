from .models import Script


def scripts_processor(request):
    """
    Контекстный процессор для добавления скриптов в шаблоны
    """
    active_scripts = Script.objects.filter(is_active=True).order_by('position', 'order')
    
    scripts_by_position = {
        'head': [],
        'body_start': [],
        'body_end': [],
        'footer': []
    }
    
    for script in active_scripts:
        scripts_by_position[script.position].append(script)
    
    return {
        'scripts_head': scripts_by_position['head'],
        'scripts_body_start': scripts_by_position['body_start'],
        'scripts_body_end': scripts_by_position['body_end'],
        'scripts_footer': scripts_by_position['footer'],
    }