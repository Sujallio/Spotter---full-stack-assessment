from django.contrib import admin
from .models import Trip, ELDLog


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'pickup_location', 'dropoff_location', 'route_distance', 'current_cycle_used', 'created_at']
    list_filter = ['created_at', 'current_cycle_used']
    search_fields = ['pickup_location', 'dropoff_location', 'current_location']
    readonly_fields = ['created_at', 'updated_at', 'route_distance', 'estimated_duration']


@admin.register(ELDLog)
class ELDLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'trip', 'log_date', 'status', 'location', 'miles_driven', 'created_at']
    list_filter = ['status', 'log_date', 'trip']
    search_fields = ['trip__pickup_location', 'location']
    readonly_fields = ['created_at']
