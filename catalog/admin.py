import re

from django.contrib import admin
from catalog.admin_filters import DropdownFilter, RelatedOnlyDropdownFilter, CategoryRelatedOnlyDropdownFilter

from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from catalog.models import CategoryImage, CategoryFile, Brand, Category, Offer
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


class FilesInline(admin.TabularInline):
    extra = 0
    autocomplete_fields = ('file', )

    def get_queryset(self, request, *args, **kwargs):
        qs = super().get_queryset(request).select_related('file')
        try:
            # extracting category_id from path
            category_id = int(re.search(r'/(\d+)/change/', request.path).group(1))
            return qs.filter(id=category_id)
        except Exception as error:
            print("Cannot overwrite get_queryset for CategoryImageInline", error)
            return qs


class CategoryImageInline(FilesInline):
    model = CategoryImage


class CategoryFileInline(FilesInline):
    model = CategoryFile


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


class CategoryAdmin(admin.ModelAdmin):
    list_select_related = ['brand']
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
        ('brand', RelatedOnlyDropdownFilter),
        ('parents', CategoryRelatedOnlyDropdownFilter),
        'status',
        'is_final'
    )
    fields = [
        'name',
        'description',
        'logo',
        'banner',
        'instruction',
        'parents',
        'brand',
        'slug',
        'place',
        'status',
        'is_final'
    ]
    filter_horizontal = ('parents', )
    autocomplete_fields = ('brand', 'certificate')
    inlines = [OfferInline, CategoryImageInline, CategoryFileInline]
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        qs = form.base_fields['parents'].queryset
        form.base_fields['parents'].queryset = qs.select_related('brand').all()
        return form


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
        ('category', CategoryRelatedOnlyDropdownFilter),
        'status'
    )
    fields = [
        'name',
        'description',
        'tech_info',
        'ctru',
        'category',
        'place',
        'status'
    ]
    autocomplete_fields = ['category']
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'category__brand')

    @admin.display(description='Бренд', ordering='name')
    def brand_name(self, obj):
        return obj.category.brand.name


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
