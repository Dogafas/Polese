# load_departure_dates_from_json.py
import os
import django
import json
from datetime import date
from dotenv import load_dotenv
from routes.models import Route, RouteDepartureDate

# Настройка Django окружения
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polese.settings")
django.setup()


load_dotenv()  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Загружаем переменные окружения из файла .env")


def load_departure_dates_from_json(filename="departure_dates.json"):
    """Загружает даты отправления из JSON файла в базу данных."""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        try:
            route = Route.objects.get(
                route_id=item["route"]
            )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Получаем объект Route по ID")
            departure_date = date.fromisoformat(item["departure_date"])
            # Проверяем, существует ли уже такая дата отправления
            if not RouteDepartureDate.objects.filter(
                route=route, departure_date=departure_date
            ).exists():
                route_departure_date = RouteDepartureDate(
                    route=route, departure_date=departure_date
                )
                route_departure_date.save()
                print(f"Сохранена дата отправления: {route} - {departure_date}")
            else:
                print(f"Дата отправления уже существует: {route} - {departure_date}")

        except Route.DoesNotExist:
            print(f"Маршрут с ID {item['route']} не найден.")
        except Exception as e:
            print(f"Ошибка при обработке записи: {item}. Ошибка: {e}")


if __name__ == "__main__":
    load_departure_dates_from_json()
