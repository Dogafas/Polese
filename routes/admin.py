from django.contrib import admin
from .models import Stop, Route, RoutePoint, RouteDepartureDate
from core.admin_mixins import ShortDescriptionMixin

class RoutePointInline(admin.TabularInline):
    
    model = RoutePoint
    extra = 1
    ordering = ['order'] 

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    inlines = [RoutePointInline]

@admin.register(RoutePoint)
class RoutePointAdmin(admin.ModelAdmin):
    list_display = ('route', 'stop', 'order', 'arrival_time', 'departure_time', 'price_multiplier')
    list_filter = ('route', 'stop')
    search_fields = ('route__name', 'stop__name')
    ordering = ('route', 'order') # сортировка по маршруту и порядку
    #readonly_fields = ('created_at', 'updated_at')

@admin.register(Stop)
class StopAdmin(admin.ModelAdmin, ShortDescriptionMixin):
    list_display = ('name', 'latitude', 'longitude', 'short_description')
    search_fields = ('name', 'description')

