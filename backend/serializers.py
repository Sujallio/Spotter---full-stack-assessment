from rest_framework import serializers
from .models import Trip, ELDLog


class ELDLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ELDLog
        fields = ['id', 'log_date', 'start_time', 'end_time', 'status', 'location', 'miles_driven']


class TripSerializer(serializers.ModelSerializer):
    eld_logs = ELDLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id', 'current_location', 'current_lat', 'current_lng',
            'pickup_location', 'pickup_lat', 'pickup_lng',
            'dropoff_location', 'dropoff_lat', 'dropoff_lng',
            'current_cycle_used', 'route_distance', 'estimated_duration',
            'eld_logs', 'created_at'
        ]
