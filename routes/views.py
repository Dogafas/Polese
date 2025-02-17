from django.shortcuts import render
from .models import Route, RoutePoint, RouteDepartureDate
import calendar
from django.core.paginator import Paginator
from collections import defaultdict


def schedule_view(request):
    """
    Представление для отображения расписания маршрутов.
    """
    routes = Route.objects.all()
    paginator = Paginator(routes, 10)
    page_number = request.GET.get("page")
    routes = paginator.get_page(page_number)

    schedule_data = []

    month_names = {
        1: "январе",
        2: "феврале",
        3: "марте",
        4: "апреле",
        5: "мае",
        6: "июне",
        7: "июле",
        8: "августе",
        9: "сентябре",
        10: "октябре",
        11: "ноябре",
        12: "декабре",
    }

    for route in routes:
        route_points = (
            RoutePoint.objects.filter(route=route)
            .order_by("order")
            .select_related("stop")
        )
        departure_dates = RouteDepartureDate.objects.filter(route=route)

        departure_location = (
            route_points.first().stop.name if route_points.exists() else None
        )
        arrival_location = (
            route_points.last().stop.name if route_points.exists() else None
        )

        flights_per_month = []
        month_counts = defaultdict(int)
        for d in departure_dates:
            month = d.departure_date.month
            month_counts[month] += 1

        for month in sorted(month_counts.keys()):
            flights_per_month.append((month, month_counts[month]))

        route_data = {
            "route": route,
            "departure_location": departure_location,
            "arrival_location": arrival_location,
            "stops": [
                {
                    "name": rp.stop.name,
                    "arrival_time": rp.arrival_time,
                }
                for rp in route_points
            ],
            "departures": [
                {
                    "date": d.departure_date,
                    "day_of_week": calendar.day_name[d.departure_date.weekday()],
                    "month": calendar.month_name[d.departure_date.month],
                }
                for d in departure_dates
            ],
            "flights_per_month": flights_per_month,
            "month_names": month_names,  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Передаём словарь с названиями месяцев")
        }
        schedule_data.append(route_data)

    context = {"schedule_data": schedule_data, "paginator": paginator, "routes": routes}
    return render(request, "routes/schedule.html", context)
