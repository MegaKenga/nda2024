from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from catalog.models import Brand, Category, Offer, Specialist, Product
from files.models import ModelImage, ModelFile, InstructionsFile, CatalogFile
from catalog.admin_filters import (
    DropdownFilter,
    RelatedOnlyDropdownFilter,
    CategoryRelatedOnlyDropdownFilter,
    ProductRelatedOnlyDropdownFilter
)


"""Общие методы админки"""


class MyAdminSite(AdminSite):
    def get_app_list(self, request, app_label=None):
        """Возвращает отсортированный список зарегистрированных приложений"""
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())
        return app_list


admin.site = MyAdminSite()

admin.site.empty_value_display = "---- ОТСУТСТВУЕТ"


class OfferInline(admin.TabularInline):
    model = Offer
    can_delete = True
    extra = 0
    show_change_link = True
    classes = ["collapse", "wide"]
    fields = [
        "name",
        "text_description",
        "shipping_pack",
        "status",
    ]


class ProductImageInline(admin.TabularInline):
    model = ModelImage
    readonly_fields = ("image_preview",)


class ProductFileInline(admin.TabularInline):
    model = ModelFile


class CategoryImageInline(admin.TabularInline):
    model = ModelImage
    readonly_fields = ("image_preview",)


class CategoryFileInline(admin.TabularInline):
    model = ModelFile


class InstructionsFileInline(admin.TabularInline):
    model = InstructionsFile


class CatalogFileInline(admin.TabularInline):
    model = CatalogFile


""""Классы админки"""


class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "place", "status", "banner_color")
    list_editable = ("place", "slug", "status", "banner_color")
    list_filter = (("name", DropdownFilter), "status")
    fields = [
        "name",
        "description",
        "logo",
        "banner_color",
        "title",
        "ceo_description",
        "keywords",
        "place",
        "slug",
        "status",
    ]
    save_as = True
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ["name"]


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ["brand"]
    list_display = ("name", "brand", "slug", "place", "status",)
    list_editable = ("place", "slug", "status")
    list_filter = (
        ("brand", RelatedOnlyDropdownFilter),
        ("parents", CategoryRelatedOnlyDropdownFilter),
        "status",
    )
    fields = [
        "name",
        "brand",
        "parents",
        "logo",
        "banner_color",
        "title",
        "ceo_description",
        "keywords",
        "place",
        "slug",
        "status",
    ]
    filter_horizontal = ("parents",)
    autocomplete_fields = ("brand",)
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ["name"]

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        qs = form.base_fields["parents"].queryset
        form.base_fields["parents"].queryset = qs.select_related("brand").all()
        return form


class ProductAdmin(admin.ModelAdmin):
    list_select_related = True
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "brand"]
    list_filter = [
        ("brand", RelatedOnlyDropdownFilter),
        ("category", CategoryRelatedOnlyDropdownFilter),
        "status",
    ]
    search_fields = ["name"]
    inlines = [
        OfferInline,
        ProductImageInline,
        ProductFileInline,
        InstructionsFileInline,
        CatalogFileInline,
    ]
    fields = [
        "name",
        "brand",
        "short_description",
        "full_description",
        "category",
        "logo",
        "specialist",
        "youtube_link",
        "rutube_link",
        "title",
        "ceo_description",
        "keywords",
        "place",
        "slug",
        "status",
    ]
    filter_horizontal = ("category",)
    autocomplete_fields = ("brand",)
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25


class OfferAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        "name",
        "brand_name",
        "product",
        "place",
        "status",
    )
    list_editable = ("place", "status")
    list_filter = (
        ("product__brand", RelatedOnlyDropdownFilter),
        ("product", ProductRelatedOnlyDropdownFilter),
        "status",
    )
    fields = [
        "name",
        "product",
        "text_description",
        "shipping_pack",
        "place",
        "status",
    ]
    autocomplete_fields = ["product"]
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ["name"]

    def get_queryset(self, request):
        return (
            super().get_queryset(request).select_related("product", "product__brand")
        )

    @admin.display(description="Бренд", ordering="name")
    def brand_name(self, obj):
        if getattr(obj, "product"):
            if obj.product.brand:
                return obj.product.brand.name
        elif hasattr(obj, "brand"):
            return obj.brand.name
        else:
            return "Бренда нет"


class SpecialistAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email")
    search_fields = ("name", "phone", "email")


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Specialist, SpecialistAdmin)



