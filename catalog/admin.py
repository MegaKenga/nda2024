from django.contrib import admin
from django.contrib.admin.filters import RelatedOnlyFieldListFilter  # необходимо для отображения только объектов, имеющих foreign key, с конкретными related_names

from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from catalog.models import Brand, ProductGroup, Category, Offer


"""Общие методы админки"""


class MyAdminSite(AdminSite):
    def get_app_list(self, request):
        """Возвращает отсортированный список зарегистрированных приложений"""
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        return app_list


admin.site = MyAdminSite()

""""Классы админки"""


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'place',
        'is_active'
    )
    list_editable = ('place', 'is_active')
    list_filter = ('name', 'is_active')
    fields = [
        'name',
        'description',
        'place',
        'is_active'
    ]
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'parent',
        'place',
        'is_active'
    )
    list_editable = ('place', 'is_active')
    list_filter = (
        'name',
        ('brand', RelatedOnlyFieldListFilter),
        ('parent', RelatedOnlyFieldListFilter),
        'is_active'
    )
    fields = [
        'name',
        'description',
        'brand',
        'parent',
        'place',
        'is_active'
    ]
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ('name', 'parent')


class ProductGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'get_categories',
        'place',
        'is_active'
    )
    list_editable = ('place', 'is_active')
    list_filter = (
        ('brand', RelatedOnlyFieldListFilter),
        ('categories', RelatedOnlyFieldListFilter),
        'is_active'
    )
    fields = [
        'name',
        'description',
        'brand',
        'categories',
        'place',
        'is_active'
    ]
    actions_on_bottom = True
    list_per_page = 25
    search_fields = (
        'name',
        'group',
        'category'
    )

    @admin.display(description='Категории, к которым принадлежит группа товаров', ordering='name')
    def get_categories(self, obj):
        if obj.categories.all():
            return list(obj.categories.all().values_list('name', flat=True))


class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand_name',
        'product_group',
        'place',
        'is_active'
    )
    list_editable = ('place', 'is_active')
    list_filter = (
        ('product_group__brand', RelatedOnlyFieldListFilter),
        ('product_group', RelatedOnlyFieldListFilter),
        'is_active'
    )
    fields = [
        'name',
        'description',
        'product_group',
        'place',
        'is_active'
    ]
    actions_on_bottom = True
    list_per_page = 25
    search_fields = (
        'name',
        'product_group'
    )

    @admin.display(description='Бренд', ordering='name')
    def brand_name(self, obj):
        return obj.product_group.brand.name


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
