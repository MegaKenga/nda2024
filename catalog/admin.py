from django.contrib import admin
from nda.filters import SimpleDropdownFilter, DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter, RelatedOnlyDropdownFilter

from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from catalog.models import Brand, ProductGroup, Category, Offer


"""Общие методы админки"""


class MyAdminSite(AdminSite):
    def get_app_list(self, request, app_label=None):
        """Возвращает отсортированный список зарегистрированных приложений"""
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        return app_list


admin.site = MyAdminSite()

admin.site.empty_value_display = '--- ОТСУТСТВУЕТ'


class CategoryInline(admin.TabularInline):
    model = Category
    can_delete = True
    extra = 0
    show_change_link = True
    classes = ['collapse', 'wide']


class ProductGroupInline(admin.TabularInline):
    model = ProductGroup
    can_delete = True
    extra = 0
    show_change_link = True
    classes = ['collapse', 'wide']


class OfferInline(admin.TabularInline):
    model = Offer
    can_delete = True
    extra = 0
    show_change_link = True
    classes = ['collapse', 'wide']


class CategoryGroupInline(admin.TabularInline):
    model = ProductGroup.categories.through
    can_delete = True
    extra = 0
    show_change_link = True
    verbose_name_plural = 'Связанные категории и группы товаров'
    classes = ['collapse', 'wide']


class CategoryCategoryInline(admin.TabularInline):
    model = Category
    can_delete = True
    extra = 0
    show_change_link = True
    verbose_name_plural = 'Связанные категории'
    classes = ['collapse', 'wide']

""""Классы админки"""


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'place',
        'is_active'
    )
    list_editable = ('place', 'is_active')
    list_filter = (('name', DropdownFilter), 'is_active')
    fields = [
        'name',
        'description',
        'place',
        'is_active'
    ]
    inlines = [CategoryInline, ProductGroupInline]
    # view_on_site = True  включить после добавления get_absolute_url
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']


class CategoryAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'name',
        'brand',
        'parent',
        'place',
        'is_active'
    )
    list_editable = ('place', 'is_active')
    list_filter = (
        ('name', DropdownFilter),
        ('brand', RelatedOnlyDropdownFilter),
        ('parent', RelatedOnlyDropdownFilter),
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
    autocomplete_fields = ['parent']
    inlines = [CategoryGroupInline, CategoryCategoryInline]
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']


class ProductGroupAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'name',
        'brand',
        'get_categories',
        'place',
        'is_active'
    )
    list_editable = ('place', 'is_active')
    list_filter = (
        ('brand', RelatedOnlyDropdownFilter),
        ('categories', RelatedOnlyDropdownFilter),
        'is_active'
    )
    filter_horizontal = ('categories', )
    fields = [
        'name',
        'description',
        'brand',
        'categories',
        'place',
        'is_active'
    ]
    inlines = [CategoryGroupInline, OfferInline]
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']

    @admin.display(description='Категории, к которым принадлежит группа товаров', ordering='name')
    def get_categories(self, obj):
        if obj.categories.all():
            return list(obj.categories.all().values_list('name', flat=True))


class OfferAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'name',
        'brand_name',
        'product_group',
        'place',
        'is_active'
    )
    list_editable = ('place', 'is_active')
    list_filter = (
        ('product_group__brand', RelatedOnlyDropdownFilter),
        ('product_group', RelatedOnlyDropdownFilter),
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
    search_fields = ['name']

    @admin.display(description='Бренд', ordering='name')
    def brand_name(self, obj):
        return obj.product_group.brand.name


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
