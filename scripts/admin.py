from django.contrib import admin
from django.utils.html import format_html
from .models import Script


# @admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'position', 
        'is_active', 
        'order', 
        'preview_code',
        'updated_at'
    ]
    
    list_filter = [
        'position', 
        'is_active', 
        'created_at'
    ]
    
    list_editable = [
        'is_active', 
        'order'
    ]
    
    search_fields = [
        'name', 
        'description'
    ]
    
    fields = [
        'name',
        'description', 
        'code',
        'position',
        'is_active',
        'order'
    ]
    
    ordering = ['position', 'order', 'name']
    
    def preview_code(self, obj):
        """Показывает превью кода в админке"""
        if obj.code:
            preview = obj.code[:100] + '...' if len(obj.code) > 100 else obj.code
            return format_html('<code style="font-size: 11px;">{}</code>', preview)
        return '-'
    
    preview_code.short_description = 'Превью кода'
    
    class Media:
        css = {
            'all': ('admin/css/scripts_admin.css',)
        }

admin.site.register(Script, ScriptAdmin)