from django.contrib import admin
from .models import Voyage, VoyageStopPrice
from core.admin_mixins import ShortDescriptionMixin


@admin.register(Voyage)
class VoyageAdmin(ShortDescriptionMixin, admin.ModelAdmin):
    list_display = ('route', 'ship', 'base_price', 'available_seats', 'status')
    ordering = ('route',)

@admin.register(VoyageStopPrice)
class VoyageStopPriceAdmin(ShortDescriptionMixin, admin.ModelAdmin):
    list_display = ('voyage', 'stop', 'price')
    ordering = ('voyage', 'stop')    