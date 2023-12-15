from django.contrib import admin
from django.contrib.admin.filters import RelatedOnlyFieldListFilter # необходимо для отображения только объектов, имеющих foreign key, с конкретными related_names
from mptt.admin import MPTTModelAdmin

from catalog.models import Brand, Product, Category


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    list_filter = ('name', 'is_active')
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']


class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 40
    list_display = ('name', 'parent', 'is_active')
    list_filter = ('name', 'is_active')
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ('name', 'parent')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'is_active')
    list_filter = (('brand', RelatedOnlyFieldListFilter), 'category', 'is_active')
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ('name', 'group', 'category')


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
