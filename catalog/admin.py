from django.contrib import admin
from django.contrib.admin.filters import RelatedOnlyFieldListFilter # необходимо для отображения только объектов, имеющих foreign key, с конкретными related_names
from django.utils.translation import gettext_lazy
from django.contrib.admin import SimpleListFilter, AdminSite
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


class IsActiveStatusFilter(SimpleListFilter):
    title = gettext_lazy('Статус показа на страницах')
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            (None, gettext_lazy('Активные')),
            # ('True', gettext_lazy('Активные')),
            ('False', gettext_lazy('Неактивные')),
            ('all', gettext_lazy('All')),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() in ('True', 'False'):
            return queryset.filter(is_active=self.value())
        elif self.value() is None:
            return queryset.filter(is_active='True')


def make_active(modeladmin, request, queryset):
    queryset.update(is_active='True')
    rows_updated = queryset.update(is_active='True')
    if rows_updated == 1:
        message_bit = "1 поле"
    else:
        message_bit = "%s полей" % rows_updated
    modeladmin.message_user(request, "%s успешно обновлено." % message_bit)


make_active.short_description = "Изменить статус на 'Активный'"


def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active='False')
    rows_updated = queryset.update(is_active='False')
    if rows_updated == 1:
        message_bit = "1 поле"
    else:
        message_bit = "%s полей" % rows_updated
    modeladmin.message_user(request, "%s успешно обновлено." % message_bit)


make_inactive.short_description = "Изменить статус на 'Неактивный'"


""""Классы админки"""


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'place',
        'is_active'
    )
    list_editable = ('place', 'is_active')
    list_filter = ('name', IsActiveStatusFilter)
    fields = [
        'name',
        'description',
        'place',
        'is_active'
    ]
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']
    actions = [make_active, make_inactive]


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
        IsActiveStatusFilter
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
    actions = [make_active, make_inactive]


class ProductGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'place',
        'is_active'
    )
    list_editable = ('place', 'is_active')
    list_filter = (
        ('brand', RelatedOnlyFieldListFilter),
        ('categories', RelatedOnlyFieldListFilter),
        IsActiveStatusFilter
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
    actions = [make_active, make_inactive]


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
        IsActiveStatusFilter
    )
    fields = [
        'name',
        'description',
        #'brand',
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
    actions = [make_active, make_inactive]

    def brand_name(self, obj):
        return obj.product_group.brand.name

    brand_name.short_description = 'Бренд'


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
