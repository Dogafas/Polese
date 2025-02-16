from django.db import models
from django.core.validators import MinValueValidator
from routes.models import Route, Stop
from ships.models import Ship


class Voyage(models.Model):
    voyage_id = models.AutoField(primary_key=True, verbose_name="ID рейса")
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, verbose_name="Судно")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="Маршрут")
    base_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Базовая цена"
    )
    available_seats = models.IntegerField(
        verbose_name="Доступные места", validators=[MinValueValidator(0)]
    )
    status = models.CharField(max_length=50, verbose_name="Статус")

    def __str__(self):
        return f"{self.route.name}"

    class Meta:
        verbose_name = "Рейс"
        verbose_name_plural = "Рейсы"


class VoyageStopPrice(models.Model):
    voyage_stop_price_id = models.AutoField(
        primary_key=True, verbose_name="ID стоимости рейса до остановки"
    )
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE, verbose_name="Рейс")
    stop = models.ForeignKey(
        Stop, on_delete=models.CASCADE, verbose_name="Остановочный пункт"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"Цена для {self.voyage} до {self.stop}: {self.price}"

    class Meta:
        verbose_name = "Стоимость билета до остановки"
        verbose_name_plural = "Стоимости билета до остановки"
