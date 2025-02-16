from django.contrib import admin
from .models import Ship
from core.admin_mixins import ShortDescriptionMixin


@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin, ShortDescriptionMixin):
    list_display = ("ship_id", "name", "capacity", "short_description")
    verbose_name = "Судно"
    verbose_name_plural = "Судно"
