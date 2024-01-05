from django.contrib import admin
from nda.filters import SimpleDropdownFilter, DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter, RelatedOnlyDropdownFilter

from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from catalog.models import Unit, Brand, Category, Offer


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


class OfferInline(admin.TabularInline):
    model = Offer
    can_delete = True
    extra = 0
    show_change_link = True
    classes = ['collapse', 'wide']


""""Классы админки"""


class UnitAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'parent',
        'place',
        'status'
    )
    list_editable = ('place', 'status')
    list_filter = (('name', DropdownFilter), ('parent', RelatedOnlyDropdownFilter), 'status')
    fields = [
        'name',
        'description',
        'parent',
        'place',
        'status'
    ]
    inlines = [CategoryInline]
    # view_on_site = True  включить после добавления get_absolute_url
    autocomplete_fields = ['parent']
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'place',
        'status'
    )
    list_editable = ('place', 'status')
    list_filter = (('name', DropdownFilter), 'status')
    fields = [
        'name',
        'description',
        'place',
        'status'
    ]
    # inlines = [CategoryInline]   очень долго грузится из за огромного количества категорий, надо еще поразбираться.
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
        'unit',
        'place',
        'status',
        'is_final'
    )
    list_editable = ('place', 'status')
    list_filter = (
        ('name', DropdownFilter),
        ('brand', RelatedOnlyDropdownFilter),
        ('parent', RelatedOnlyDropdownFilter),
        'status',
        'is_final'
    )
    fields = [
        'name',
        'description',
        'brand',
        'unit',
        'parent',
        'place',
        'status',
        'is_final'
    ]
    inlines = [CategoryInline, OfferInline]
    autocomplete_fields = ['parent', 'unit']
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']


class OfferAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'name',
        'brand_name',
        'category',
        'place',
        'status'
    )
    list_editable = ('place', 'status')
    list_filter = (
        ('category__brand', RelatedOnlyDropdownFilter),
        ('category', RelatedOnlyDropdownFilter),
        'status'
    )
    fields = [
        'name',
        'description',
        'category',
        'place',
        'status'
    ]
    autocomplete_fields = ['category']
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']

    @admin.display(description='Бренд', ordering='name')
    def brand_name(self, obj):
        return obj.category.brand.name


admin.site.register(Unit, UnitAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
