from django.db import models
from django.utils import timezone

class Trip(models.Model):
    current_location = models.CharField(max_length=255)
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)
    
    pickup_location = models.CharField(max_length=255)
    pickup_lat = models.FloatField(null=True, blank=True)
    pickup_lng = models.FloatField(null=True, blank=True)
    
    dropoff_location = models.CharField(max_length=255)
    dropoff_lat = models.FloatField(null=True, blank=True)
    dropoff_lng = models.FloatField(null=True, blank=True)
    
    current_cycle_used = models.FloatField(default=0)  # Hours
    route_distance = models.FloatField(null=True, blank=True)  # Miles
    estimated_duration = models.FloatField(null=True, blank=True)  # Hours
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Trip from {self.pickup_location} to {self.dropoff_location}"


class ELDLog(models.Model):
    STATUS_CHOICES = [
        ('OFF', 'Off Duty'),
        ('SB', 'Sleeper Berth'),
        ('DRIVING', 'Driving'),
        ('ON', 'On Duty (Not Driving)'),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='eld_logs')
    log_date = models.DateField()
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    location = models.CharField(max_length=255, blank=True)
    miles_driven = models.FloatField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['log_date', 'start_time']
    
    def __str__(self):
        return f"ELD Log - {self.trip} - {self.log_date}"
