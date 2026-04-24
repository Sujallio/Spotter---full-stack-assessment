import requests
import time
from datetime import datetime, timedelta
from .models import ELDLog, Trip

class ELDLogGenerator:
    """Generate ELD logs based on HOS regulations"""
    
    HOS_LIMITS = {
        'max_driving_hours': 11,  # 11 hours driving
        'max_on_duty_hours': 14,  # 14 hours on duty
        'max_cycle_hours': 70,  # 70 hours in 8 days
        'min_rest_hours': 10,  # 10 hour off-duty or sleeper
        'required_break_after_hours': 8,  # 8 hour break after 8 hours driving
    }
    
    FUEL_STOP_INTERVAL = 1000  # miles
    FUEL_STOP_DURATION = 0.5  # hours
    PICKUP_DURATION = 1  # hour
    DROPOFF_DURATION = 1  # hour
    DRIVING_SPEED = 60  # mph average
    
    def __init__(self, trip):
        self.trip = trip
        self.logs = []
        self.current_time = datetime.now()
        self.total_distance = trip.route_distance or 0
        self.current_cycle_used = trip.current_cycle_used
        self.cycle_start_date = self.current_time.date()
        
    def generate_logs(self):
        """Generate ELD logs for the entire trip"""
        # Start with pickup
        self._add_pickup_log()
        
        # Calculate route segments with fuel stops
        remaining_distance = self.total_distance
        distance_since_fuel = 0
        
        while remaining_distance > 0:
            # Check HOS limits
            if self._is_cycle_exceeded():
                self._add_rest_log(10)  # 10 hour rest
            
            # Drive until fuel stop or trip end
            drive_distance = min(remaining_distance, self.FUEL_STOP_INTERVAL - distance_since_fuel)
            drive_hours = drive_distance / self.DRIVING_SPEED
            
            # Check daily driving limits
            if drive_hours > self._get_remaining_driving_hours():
                drive_hours = self._get_remaining_driving_hours()
                drive_distance = drive_hours * self.DRIVING_SPEED
            
            if drive_distance > 0:
                self._add_driving_log(drive_distance, drive_hours)
                remaining_distance -= drive_distance
                distance_since_fuel += drive_distance
            
            # Fuel stop if more distance remains
            if remaining_distance > 0 and distance_since_fuel >= self.FUEL_STOP_INTERVAL:
                self._add_fuel_stop_log()
                distance_since_fuel = 0
            
            # Check if we need rest
            if self._needs_rest():
                break
        
        # Add dropoff
        if remaining_distance <= 0:
            self._add_dropoff_log()
        
        return self.logs
    
    def _add_pickup_log(self):
        """Add pickup location log"""
        log = ELDLog(
            trip=self.trip,
            log_date=self.current_time.date(),
            start_time=self.current_time,
            end_time=self.current_time + timedelta(hours=self.PICKUP_DURATION),
            status='ON',
            location=self.trip.pickup_location,
            miles_driven=0
        )
        log.save()
        self.logs.append(log)
        self.current_time += timedelta(hours=self.PICKUP_DURATION)
        self.current_cycle_used += self.PICKUP_DURATION
    
    def _add_dropoff_log(self):
        """Add dropoff location log"""
        log = ELDLog(
            trip=self.trip,
            log_date=self.current_time.date(),
            start_time=self.current_time,
            end_time=self.current_time + timedelta(hours=self.DROPOFF_DURATION),
            status='ON',
            location=self.trip.dropoff_location,
            miles_driven=0
        )
        log.save()
        self.logs.append(log)
        self.current_time += timedelta(hours=self.DROPOFF_DURATION)
        self.current_cycle_used += self.DROPOFF_DURATION
    
    def _add_driving_log(self, distance, hours):
        """Add driving log"""
        log = ELDLog(
            trip=self.trip,
            log_date=self.current_time.date(),
            start_time=self.current_time,
            end_time=self.current_time + timedelta(hours=hours),
            status='DRIVING',
            location='In Transit',
            miles_driven=distance
        )
        log.save()
        self.logs.append(log)
        self.current_time += timedelta(hours=hours)
        self.current_cycle_used += hours
    
    def _add_fuel_stop_log(self):
        """Add fuel stop log"""
        log = ELDLog(
            trip=self.trip,
            log_date=self.current_time.date(),
            start_time=self.current_time,
            end_time=self.current_time + timedelta(hours=self.FUEL_STOP_DURATION),
            status='ON',
            location='Fuel Stop',
            miles_driven=0
        )
        log.save()
        self.logs.append(log)
        self.current_time += timedelta(hours=self.FUEL_STOP_DURATION)
        self.current_cycle_used += self.FUEL_STOP_DURATION
    
    def _add_rest_log(self, hours):
        """Add rest/off-duty log"""
        log = ELDLog(
            trip=self.trip,
            log_date=self.current_time.date(),
            start_time=self.current_time,
            end_time=self.current_time + timedelta(hours=hours),
            status='OFF',
            location='Rest',
            miles_driven=0
        )
        log.save()
        self.logs.append(log)
        self.current_time += timedelta(hours=hours)
        self.current_cycle_used = 0  # Reset cycle after rest
        self.cycle_start_date = self.current_time.date()
    
    def _get_remaining_driving_hours(self):
        """Get remaining driving hours for the day"""
        return max(0, self.HOS_LIMITS['max_driving_hours'])
    
    def _is_cycle_exceeded(self):
        """Check if 70-hour cycle is exceeded"""
        return self.current_cycle_used >= self.HOS_LIMITS['max_cycle_hours']
    
    def _needs_rest(self):
        """Check if driver needs rest"""
        return self.current_cycle_used >= self.HOS_LIMITS['max_cycle_hours'] - 1


class RouteCalculator:
    """Calculate route using OpenStreetMap Nominatim API"""
    
    NOMINATIM_URL = "https://nominatim.openstreetmap.org"
    OSRM_URL = "https://router.project-osrm.org"
    
    @staticmethod
    def geocode_location(location_name):
        """Convert location name to coordinates"""
        try:
            headers = {
                'User-Agent': 'ELD-Trip-Planner/1.0 (Educational Use)'
            }
            params = {
                'q': location_name,
                'format': 'json',
                'limit': 1
            }
            response = requests.get(
                f"{RouteCalculator.NOMINATIM_URL}/search", 
                params=params, 
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    result = data[0]
                    lat = float(result['lat'])
                    lon = float(result['lon'])
                    print(f"✅ Geocoded '{location_name}' to ({lat}, {lon})")
                    return lat, lon
                else:
                    print(f"⚠️ No results found for '{location_name}'")
            else:
                print(f"⚠️ Nominatim API error: {response.status_code}")
        except Exception as e:
            print(f"❌ Geocoding error for '{location_name}': {e}")
        return None, None
    
    @staticmethod
    def calculate_route(start_coords, end_coords):
        """Calculate route distance using OSRM"""
        try:
            if not start_coords or not end_coords:
                print("❌ Invalid coordinates provided")
                return None
            
            lat1, lon1 = start_coords
            lat2, lon2 = end_coords
            
            url = f"{RouteCalculator.OSRM_URL}/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
            headers = {
                'User-Agent': 'ELD-Trip-Planner/1.0 (Educational Use)'
            }
            params = {
                'overview': 'full',
                'steps': 'true'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('routes') and len(data['routes']) > 0:
                    route = data['routes'][0]
                    distance_miles = route['distance'] / 1609.34  # Convert meters to miles
                    duration_hours = route['duration'] / 3600  # Convert seconds to hours
                    print(f"✅ Route calculated: {distance_miles:.2f} miles, {duration_hours:.2f} hours")
                    return {
                        'distance': distance_miles,
                        'duration': duration_hours,
                        'route': route
                    }
                else:
                    print("⚠️ No routes found")
            else:
                print(f"⚠️ OSRM API error: {response.status_code}")
        except Exception as e:
            print(f"❌ Route calculation error: {e}")
        
        return None
