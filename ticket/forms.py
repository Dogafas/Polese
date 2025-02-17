from django import forms
from .models import Ticket
from django.core.exceptions import ValidationError
from routes.models import RoutePoint


class TicketAdminForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "passenger",
            "voyage",
            "departure_stop",
            "arrival_stop",
            "seat_number",
            "price",
            "is_paid",
        ]

    def clean(self):
        cleaned_data = super().clean()
        voyage = cleaned_data.get("voyage")
        departure_stop = cleaned_data.get("departure_stop")
        arrival_stop = cleaned_data.get("arrival_stop")
        seat_number = cleaned_data.get("seat_number")

        if voyage and departure_stop and arrival_stop:
            # Получаем вместимость судна
            capacity = voyage.ship.capacity
            # Получаем количество доступных мест из рейса
            available_seats = voyage.available_seats

            if available_seats <= 0:
                raise ValidationError("На этот рейс все места уже заняты!")

            # Если есть seat_number проверяем что он не больше вместимости судна и не меньше 1
            if seat_number:
                if seat_number > capacity or seat_number < 1:
                    raise ValidationError(
                        f"Номер места должен быть в диапазоне от 1 до {capacity}!"
                    )

            # Получаем RoutePoint для пункта отправления
            try:
                departure_route_point = RoutePoint.objects.get(
                    route=voyage.route, stop=departure_stop
                )
            except RoutePoint.DoesNotExist:
                raise ValidationError("Пункт отправления не найден в маршруте рейса!")

            # Получаем RoutePoint для пункта прибытия
            try:
                arrival_route_point = RoutePoint.objects.get(
                    route=voyage.route, stop=arrival_stop
                )
            except RoutePoint.DoesNotExist:
                raise ValidationError("Пункт прибытия не найден в маршруте рейса!")
            # Проверяем, что порядок пункта отправления меньше порядка пункта прибытия
            if departure_route_point.order >= arrival_route_point.order:
                raise ValidationError("Вы выбрали противоположный маршрут!")

        return cleaned_data
