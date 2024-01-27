from django.contrib import admin
from nda.filters import DropdownFilter, RelatedOnlyDropdownFilter

from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from catalog.models import Brand, Category, CategoryImage, Offer
# from files.admin import OfferImageInline


"""Общие методы админки"""


class MyAdminSite(AdminSite):
    def get_app_list(self, request, app_label=None):
        """Возвращает отсортированный список зарегистрированных приложений"""
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        return app_list


admin.site = MyAdminSite()

admin.site.empty_value_display = '---- ОТСУТСТВУЕТ'


class OfferInline(admin.TabularInline):
    model = Offer
    can_delete = True
    extra = 0
    show_change_link = True
    classes = ['collapse', 'wide']


class CategoryInline(admin.TabularInline):
    model = Category
    can_delete = True
    extra = 0
    show_change_link = True
    classes = ['collapse', 'wide']


""""Классы админки"""


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'place',
        'status'
    )
    list_editable = ('place', 'slug', 'status')
    list_filter = (('name', DropdownFilter), 'status')
    fields = [
        'name',
        'description',
        'slug',
        'place',
        'status',
        'logo',
        'banner'
    ]
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']


class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'name',
        'brand',
        'slug',
        'place',
        'status',
        'is_final'
    )
    list_editable = ('place', 'slug', 'status')
    list_filter = (
        ('name', DropdownFilter),
        ('brand', RelatedOnlyDropdownFilter),
        ('parents', RelatedOnlyDropdownFilter),
        'status',
        'is_final'
    )
    fields = [
        'name',
        'description',
        # 'logo',
        # 'banner',
        'certificate',
        'instruction',
        'parents',
        'brand',
        'slug',
        'place',
        'status',
        'is_final'
    ]
    filter_horizontal = ('parents', )
    inlines = [OfferInline, CategoryImageInline]
    view_on_site = True
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
        'picture',
        'tech_info',
        'ctru',
        'category',
        'place',
        'status'
    ]
    autocomplete_fields = ['category']
    # inlines = [OfferImageInline]
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']

    @admin.display(description='Бренд', ordering='name')
    def brand_name(self, obj):
        return obj.category.brand.name


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
