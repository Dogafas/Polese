from django.shortcuts import render
from .models import Route, RoutePoint, RouteDepartureDate
import calendar  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Импортируем модуль calendar для работы с датами")
from datetime import datetime  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Импортируем datetime")


def schedule_view(request):
    """
    Представление для отображения расписания маршрутов.
    """
    routes = Route.objects.all()  # Получаем все маршруты
    schedule_data = []

    for route in routes:
        route_points = (
            RoutePoint.objects.filter(route=route)
            .order_by("order")
            .select_related("stop")
        )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Улучшаем запрос, чтобы получить данные об остановках сразу")
        departure_dates = RouteDepartureDate.objects.filter(route=route)

        # Формируем данные для шаблона
        route_data = {
            "route": route,
            "stops": [
                {
                    "name": rp.stop.name,
                    "arrival_time": rp.arrival_time,
                }
                for rp in route_points
            ],  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Используем данные об остановках, полученные из select_related")
            "departures": [
                {
                    "date": d.departure_date,
                    "day_of_week": calendar.day_name[d.departure_date.weekday()],
                    "month": calendar.month_name[d.departure_date.month],
                }
                for d in departure_dates
            ],
            "flights_per_month": len(departure_dates),  # общее кол-во рейсов
        }
        schedule_data.append(route_data)

    context = {"schedule_data": schedule_data}
    return render(request, "routes/schedule.html", context)
