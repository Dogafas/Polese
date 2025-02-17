# # load_routes.py
# import os
# import django
# import json
# from dotenv import load_dotenv

# # Настройка Django окружения
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polese.settings")
# django.setup()

# from routes.models import Route
# from routes.serializers import RouteSerializer

# load_dotenv()  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Загружаем переменные окружения из файла .env")


# def load_routes_data():
#     """Загружает данные о маршрутах, используя сериализатор."""
#     routes = Route.objects.all()
#     serializer = RouteSerializer(routes, many=True)
#     return serializer.data


# def write_json_file(data, filename="routes_data.json"):
#     """Записывает данные в JSON файл."""
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)
#     print(f"Данные успешно записаны в файл: {filename}")


# if __name__ == "__main__":
#     routes_data = load_routes_data()
#     write_json_file(routes_data)

# load_routes.py
import os
import django
import json
import argparse
from datetime import date, timedelta
from dotenv import load_dotenv

# Настройка Django окружения
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polese.settings")
django.setup()

from routes.models import Route, RouteDepartureDate
from routes.serializers import RouteDepartureDateSerializer

load_dotenv()


def generate_departure_dates(route, start_date, end_date, interval=2):
    """Генерирует даты отправления для маршрута до указанной даты."""
    current_date = start_date
    departure_dates = []

    while current_date <= end_date:
        # Проверяем, существует ли уже такая дата отправления
        if not RouteDepartureDate.objects.filter(
            route=route, departure_date=current_date
        ).exists():  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Проверка на существование")
            departure_dates.append(
                RouteDepartureDate(route=route, departure_date=current_date)
            )
        current_date += timedelta(days=interval)

    return departure_dates


def serialize_departure_dates(departure_dates):
    """Сериализует даты отправления."""
    serializer = RouteDepartureDateSerializer(departure_dates, many=True)
    return serializer.data


def write_json_file(data, filename="departure_dates.json"):
    """Записывает данные в JSON файл."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Данные успешно записаны в файл: {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate departure dates for routes."
    )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Добавляем парсер аргументов")
    parser.add_argument(
        "--start_date",
        type=str,
        help="Start date in YYYY-MM-DD format",
        default="2025-05-01",
    )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Аргумент для start_date")
    parser.add_argument(
        "--end_date", type=str, help="End date in YYYY-MM-DD format", required=True
    )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Аргумент для end_date (обязательный)")
    parser.add_argument(
        "--interval", type=int, help="Interval in days between departures", default=2
    )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Аргумент для interval")
    parser.add_argument(
        "--route_ids",
        type=str,
        help="Comma-separated list of route IDs to generate dates for (optional)",
        required=False,
    )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Аргумент для фильтрации по ID маршрутов")

    args = parser.parse_args()

    start_date = date.fromisoformat(
        args.start_date
    )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Преобразуем строку в дату")
    end_date = date.fromisoformat(
        args.end_date
    )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Преобразуем строку в дату")
    interval = args.interval

    all_departure_dates = []

    routes = Route.objects.all()
    if args.route_ids:  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Фильтруем маршруты, если указаны ID")
        route_ids = [int(route_id) for route_id in args.route_ids.split(",")]
        routes = routes.filter(route_id__in=route_ids)

    for route in routes:
        departure_dates = generate_departure_dates(
            route, start_date, end_date, interval
        )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Передаем start_date и end_date")
        serialized_dates = serialize_departure_dates(departure_dates)
        all_departure_dates.extend(serialized_dates)

    write_json_file(all_departure_dates, filename="departure_dates.json")
