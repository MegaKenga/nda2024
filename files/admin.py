from django.contrib import admin

from files.models import ModelImage, ModelFile, InstructionsFile, CatalogFile
from catalog.admin_filters import RelatedOnlyDropdownFilter


class ModelImageAdmin(admin.ModelAdmin):
    list_display = (
        'product',
    )
    fields = [
        'product',
        'image',
    ]
    view_on_site = True
    actions_on_bottom = True
    list_filter = (("product", RelatedOnlyDropdownFilter), )
    list_per_page = 25


class ModelFileAdmin(admin.ModelAdmin):
    list_display = (
        'product',
    )
    fields = [
        'product',
        'file',
    ]
    view_on_site = True
    actions_on_bottom = True
    list_filter = (("product", RelatedOnlyDropdownFilter), )
    list_per_page = 25


class InstructionsFileAdmin(admin.ModelAdmin):
    list_display = (
        'product',
    )
    fields = [
        'product',
        'file',
    ]
    view_on_site = True
    actions_on_bottom = True
    list_filter = (("product", RelatedOnlyDropdownFilter), )
    list_per_page = 25


class CatalogFileAdmin(admin.ModelAdmin):
    list_display = (
        'product',
    )
    fields = [
        'product',
        'file',
    ]
    view_on_site = True
    actions_on_bottom = True
    list_filter = (("product", RelatedOnlyDropdownFilter), )
    list_per_page = 25


admin.site.register(ModelImage, ModelImageAdmin)
admin.site.register(ModelFile, ModelFileAdmin)
admin.site.register(InstructionsFile, InstructionsFileAdmin)
admin.site.register(CatalogFile, CatalogFileAdmin)
