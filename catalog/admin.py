from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.db.models.fields.files import FieldFile
from django.db import models
from django.forms import Textarea
from django_ckeditor_5.widgets import CKEditor5Widget
from django_ckeditor_5.fields import CKEditor5Field

from catalog.models import Brand, Category, Offer, Specialist, Product
from files.models import ModelImage, ModelFile, InstructionsFile, CatalogFile
from catalog.admin_filters import (
    DropdownFilter,
    CategoryRelatedOnlyDropdownFilter,
    RelatedOnlyDropdownFilter,
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
        "place",
        "status",
    ]


class ProductImageInline(admin.TabularInline):
    model = ModelImage
    extra = 0
    readonly_fields = ("image_preview",)


class ProductFileInline(admin.TabularInline):
    model = ModelFile
    extra = 0


class CategoryImageInline(admin.TabularInline):
    model = ModelImage
    extra = 0
    readonly_fields = ("image_preview",)


class CategoryFileInline(admin.TabularInline):
    model = ModelFile
    extra = 0


class InstructionsFileInline(admin.TabularInline):
    model = InstructionsFile
    extra = 0


class CatalogFileInline(admin.TabularInline):
    model = CatalogFile
    extra = 0


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
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 80})},
    }
    save_as = True
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ["name"]
    save_on_top = True


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ["brand"]
    list_display = ("name", "brand", "slug", "place", "status",)
    list_editable = ("place", "slug", "status")
    list_filter = (
        ("brand", RelatedOnlyDropdownFilter),
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
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 80})},

    }
    filter_horizontal = ("parents",)
    autocomplete_fields = ("brand",)
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ["name"]
    save_on_top = True

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
        "characteristics",
        "parents",
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
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 80})},
    }
    filter_horizontal = ("parents",)
    autocomplete_fields = ("brand",)
    view_on_site = True
    actions_on_bottom = True
    save_as = True
    save_on_top = True
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('brand')

    def save_model(self, request, obj, form, change):
        # Django always sends this when "Save as new is clicked"
        if '_saveasnew' in request.POST:
            # Get the ID from the admin URL
            original_pk = request.resolver_match.kwargs['object_id']
            # Get the original object
            original_obj = obj._meta.concrete_model.objects.get(id=original_pk)

            # Iterate through all it's properties
            for prop, value in vars(original_obj).items():
                # if the property is an Image (don't forget to import ImageFieldFile!)
                if isinstance(getattr(original_obj, prop), FieldFile):
                    setattr(obj,prop,getattr(original_obj, prop)) # Copy it!
        obj.save()


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
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 80})},
    }
    autocomplete_fields = ["product"]
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ["name"]
    save_on_top = True

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
