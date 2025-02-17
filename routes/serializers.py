# routes/serializers.py
from rest_framework import serializers
from .models import Route, Stop, RoutePoint, RouteDepartureDate


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = "__all__"  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Включаем все поля")


class RoutePointSerializer(serializers.ModelSerializer):
    stop = StopSerializer(read_only=True)
    stop_id = serializers.PrimaryKeyRelatedField(
        queryset=Stop.objects.all(), source="stop", write_only=True
    )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Добавляем поле для записи ID остановки")

    class Meta:
        model = RoutePoint
        fields = "__all__"  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Включаем все поля")
        read_only_fields = ["route"]  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("route только для чтения")


class RouteDepartureDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteDepartureDate
        fields = "__all__"  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Включаем все поля")


class RouteSerializer(serializers.ModelSerializer):
    routepoint_set = RoutePointSerializer(many=True, read_only=True)
    routedeparturedate_set = RouteDepartureDateSerializer(
        many=True, read_only=True
    )  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Включаем RouteDepartureDate")

    class Meta:
        model = Route
        fields = "__all__"  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: ("Включаем все поля")
