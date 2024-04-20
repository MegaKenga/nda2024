from django.contrib import admin
from files.models import ModelImage, ModelFile


class ModelImageAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'image')
    actions_on_bottom = True
    list_per_page = 25


class ModelFileAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'file')
    actions_on_bottom = True
    list_per_page = 25


admin.site.register(ModelImage, ModelImageAdmin)
admin.site.register(ModelFile, ModelFileAdmin)
