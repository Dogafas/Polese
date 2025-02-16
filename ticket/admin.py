from django.contrib import admin
from .models import Ticket
from .forms import TicketAdminForm


class TicketAdmin(admin.ModelAdmin):
    form = TicketAdminForm  # Указываем кастомную форму
    list_display = (
        "voyage",
        "departure_stop",
        "arrival_stop",
        "seat_number",
        "created_at",
        "updated_at",
        "is_paid",
    )
    list_filter = ("voyage", "is_paid")
    search_fields = ("voyage__name", "departure_stop__name", "arrival_stop__name")
    list_per_page = 20


admin.site.register(Ticket, TicketAdmin)
