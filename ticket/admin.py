from pyexpat.errors import messages
from django.contrib import admin, messages
from .models import Ticket
from .forms import TicketAdminForm 

class TicketAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'seat_number','departure_stop', 'arrival_stop', 'voyage', 'price', 'purchase_date', 'status', )
    readonly_fields = ('seat_number',)
    form = TicketAdminForm
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        """
        При создании нового билета назначаем номер места.
        """
        try:
            if obj.seat_number is None: # Если номер места не назначен
                obj.assign_seat() #  Назначаем место
            super().save_model(request, obj, form, change)
            self.message_user(request, f"Билет успешно оформлен! Номер вашего места: {obj.seat_number}",
                              level=messages.SUCCESS)
        except ValueError as e:
            # Обработка ситуации, когда нет доступных мест
            self.message_user(request, str(e), level='ERROR')

admin.site.register(Ticket, TicketAdmin)