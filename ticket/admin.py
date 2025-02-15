from pyexpat.errors import messages
from django.contrib import admin, messages
from .models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'voyage', 'passenger', 'seat_number', 'price', 'purchase_date', 'status')
    readonly_fields = ('seat_number',) 

    def save_model(self, request, obj, form, change):
        """
        При создании нового билета назначаем номер места.
        """
        super().save_model(request, obj, form, change)
        try:
            obj.assign_seat()
            self.message_user(request, f"Билет успешно оформлен! Номер вашего места: {obj.seat_number}", 
                              level=messages.SUCCESS)
        except ValueError as e:
            # Обработка ситуации, когда нет доступных мест
            self.message_user(request, str(e), level='ERROR')

admin.site.register(Ticket, TicketAdmin)