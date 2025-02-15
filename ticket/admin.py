from django.contrib import admin
from .models import Ticket
from core.admin_mixins import ShortDescriptionMixin

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin, ShortDescriptionMixin):
    list_display = ('ticket_id', 'voyage', 'passenger', 'seat_number', 'price', 'purchase_date', 'status', 'qr_code', 'short_description')
    verbose_name = 'Билет'
    verbose_name_plural = 'Билеты'