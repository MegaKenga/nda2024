from django.contrib import admin
from files.models import CatalogImage


class CatalogImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    actions_on_bottom = True
    list_per_page = 25


admin.site.register(CatalogImage, CatalogImageAdmin)
