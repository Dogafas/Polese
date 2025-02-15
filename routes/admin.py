from django.contrib import admin
from .models import Stop, Route, RoutePoint, RouteDepartureDate
from core.admin_mixins import ShortDescriptionMixin
from django.contrib.admin import DateFieldListFilter

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
    ordering = ('route', 'order')
    list_per_page = 10
    

@admin.register(Stop)
class StopAdmin(admin.ModelAdmin, ShortDescriptionMixin):
    list_display = ('name', 'latitude', 'longitude', 'short_description')
    search_fields = ('name', 'description')

@admin.register(RouteDepartureDate)
class RouteDepartureDateAdmin(admin.ModelAdmin):
    list_display = ('route', 'departure_date')
    list_filter = (('departure_date',  DateFieldListFilter), 'route')
    search_fields = ('route__name',)
    list_per_page = 10