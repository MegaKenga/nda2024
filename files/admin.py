from django.contrib import admin
from files.models import MainPage, UnitFiles, BrandFiles, CategoryFiles, OfferFiles


class MainPageAdmin(admin.ModelAdmin):
    list_display = ('banner', )
    actions_on_bottom = True
    list_per_page = 25


class UnitFilesAdmin(admin.ModelAdmin):
    list_display = (
        'unit',
        'banner',
        'image'
    )
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['unit']


class BrandFilesAdmin(admin.ModelAdmin):
    list_display = (
        'brand',
        'banner',
        'image'
    )
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['brand']


class CategoryFilesAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'banner',
        'image',
        'registration_certificate',
        'instruction'
    )
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['category']


class OfferFilesAdmin(admin.ModelAdmin):
    list_display = (
        'offer',
        'image',
        'tech_specification'
    )
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['offer']


admin.site.register(MainPage, MainPageAdmin)
admin.site.register(UnitFiles, UnitFilesAdmin)
admin.site.register(BrandFiles, BrandFilesAdmin)
admin.site.register(CategoryFiles, CategoryFilesAdmin)
admin.site.register(OfferFiles, OfferFilesAdmin)