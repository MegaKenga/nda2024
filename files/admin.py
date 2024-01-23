from django.contrib import admin
from files.models import LogoImage, BannerImage, RegistrationFile, InstructionFile, OfferImage, OfferTechDescription


"""Inlines"""


class BaseInline(admin.TabularInline):
    can_delete = True
    extra = 0
    show_change_link = True
    classes = ['collapse', 'wide']


class RegistrationInline(BaseInline):
    model = RegistrationFile


class InstructionInline(BaseInline):
    model = InstructionFile


class OfferImageInline(BaseInline):
    model = OfferImage


class OfferTechDescriptionInline(BaseInline):
    model = OfferTechDescription


"""Admin classes"""


class LogoImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    actions_on_bottom = True
    list_per_page = 25


class BannerImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    actions_on_bottom = True
    list_per_page = 25


admin.site.register(LogoImage, LogoImageAdmin)
admin.site.register(BannerImage, BannerImageAdmin)
