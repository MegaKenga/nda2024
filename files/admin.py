from django.contrib import admin
from files.models import ModelImage, ModelFile


class OfferImageInline(admin.TabularInline):
    model = ModelImage
    can_delete = True
    extra = 0
    show_change_link = True
    classes = ['collapse', 'wide']


class ModelImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    actions_on_bottom = True
    list_per_page = 25


class ModelFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')
    actions_on_bottom = True
    list_per_page = 25


admin.site.register(ModelImage, ModelImageAdmin)
admin.site.register(ModelFile, ModelFileAdmin)
