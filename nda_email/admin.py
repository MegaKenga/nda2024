from django.contrib import admin
from nda_email.models import OrderNumber

class OrderAdmin(admin.ModelAdmin):
    list_display = ("name", "value")
    fields = [
        "name",
        "value",
    ]
    save_as = True
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ["name"]
    save_on_top = True


admin.site.register(OrderNumber, OrderAdmin)
