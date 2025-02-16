from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator


class Stop(models.Model):
    stop_id = models.AutoField(primary_key=True, verbose_name="ID остановки")
    name = models.CharField(max_length=255, verbose_name="Название")
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name="Широта", null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name="Долгота", null=True, blank=True
    )
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Остановочный пункт"
        verbose_name_plural = "Остановочные пункты"


class Route(models.Model):
    route_id = models.AutoField(primary_key=True, verbose_name="ID маршрута")
    name = models.CharField(max_length=255, verbose_name="Название маршрута")
    departure_location = models.CharField(
        max_length=255, verbose_name="Пункт отправления"
    )
    arrival_location = models.CharField(max_length=255, verbose_name="Пункт прибытия")
    distance = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Расстояние, км"
    )
    duration = models.DurationField(verbose_name="Продолжительность, ч.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршрут"


class RouteDepartureDate(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="Маршрут")
    departure_date = models.DateField(verbose_name="Дата отправления")

    class Meta:
        verbose_name = "Дата отправления маршрута"
        verbose_name_plural = "Даты отправления маршрута"

    def __str__(self):
        return f"{self.route.name} - {self.departure_date}"


class RoutePoint(models.Model):
    route_point_id = models.AutoField(
        primary_key=True, verbose_name="ID точки маршрута"
    )
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="Маршрут")
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE, verbose_name="Остановка")
    order = models.IntegerField(
        verbose_name="Порядок", validators=[MinValueValidator(0)]
    )
    arrival_time = models.TimeField(verbose_name="Время прибытия")
    departure_time = models.TimeField(
        verbose_name="Время отправления", null=True, blank=True
    )
    price_multiplier = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Множитель цены",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ["order"]
        verbose_name = "Точка маршрута"
        verbose_name_plural = "Точки маршрута"
        unique_together = ("route", "order")

    def __str__(self):
        return f"{self.stop.name} ({self.route.name})"
