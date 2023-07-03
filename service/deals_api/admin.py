from django.contrib import admin

from deals_api.models import Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date')
