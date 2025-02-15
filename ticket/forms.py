from django import forms
from .models import Ticket
from voyages.models import Voyage
from django.core.exceptions import ValidationError

class TicketAdminForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'  # Или перечислите нужные поля

    def clean(self):
        cleaned_data = super().clean()
        voyage = cleaned_data.get('voyage')
        seat_number = cleaned_data.get('seat_number')

        if voyage:
            # Получаем вместимость судна
            capacity = voyage.ship.capacity
            # Получаем количество доступных мест из рейса
            available_seats = voyage.available_seats

            if available_seats <= 0:
                raise ValidationError("На этот рейс все места уже заняты!")
            
            # Если есть seat_number проверяем что он не больше вместимости судна и не меньше 1
            if seat_number:
                if seat_number > capacity or seat_number < 1:
                    raise ValidationError(f"Номер места должен быть в диапазоне от 1 до {capacity}!")

        return cleaned_data