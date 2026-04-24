# ELD Trip Planner - Technical Documentation

## Electronic Logging Device (ELD) Overview

An Electronic Logging Device is a device that records a driver's Hours of Service (HOS) to ensure compliance with federal regulations. This application automates ELD log generation based on trip details and HOS rules.

## Hours of Service (HOS) Regulations

### Federal Motor Carrier Safety Regulations (FMCSA) Part 395

#### 1. **70-Hour / 8-Day Cycle Limit**
- A driver cannot drive after 70 hours of on-duty time in any 8-day period
- Once a driver reaches 70 hours, they must take a 34-hour rest period
- This applies to property-carrying drivers

#### 2. **11-Hour Driving Limit**
- A driver cannot drive for more than 11 hours in a single shift
- Driving time is measured cumulatively in a 14-hour shift window
- After reaching 11 hours, the driver must take a 10-hour rest break

#### 3. **14-Hour Rule**
- A driver can only be on duty (driving or non-driving) for 14 consecutive hours
- After 14 hours, they must take a 10-hour off-duty rest period

#### 4. **30-Minute Break Rule**
- After driving for 8 hours without a break, the driver must take a 30-minute break
- The break can be on-duty (not driving) time
- Driving time resets to 0 after the break

#### 5. **Off-Duty Status**
- Off-duty time is not counted toward driving or on-duty limits
- A 34-hour rest period is required to reset the 70-hour cycle (only once per 8 days)
- Sleeper berth time counts as off-duty for rest purposes

## App Implementation

### Data Models

#### Trip Model
```python
class Trip:
    - current_location: CharField
    - current_lat/lng: Float
    - pickup_location: CharField
    - pickup_lat/lng: Float
    - dropoff_location: CharField
    - dropoff_lat/lng: Float
    - current_cycle_used: Float (hours)
    - route_distance: Float (miles)
    - estimated_duration: Float (hours)
```

#### ELDLog Model
```python
class ELDLog:
    - trip: ForeignKey(Trip)
    - log_date: DateField
    - start_time: DateTime
    - end_time: DateTime
    - status: CharField (OFF, SB, DRIVING, ON)
    - location: CharField
    - miles_driven: Float
```

### Status Types
- **OFF**: Off-duty (rest period)
- **SB**: Sleeper Berth (in sleeper compartment)
- **DRIVING**: Actively driving
- **ON**: On-duty not driving (fuel stops, loading, etc.)

## ELD Log Generation Algorithm

### Input
```
- Current location
- Pickup location
- Dropoff location
- Current cycle hours used
- Route distance (miles)
```

### Process

1. **Initialize**
   - Start time = current time
   - Total distance = route distance
   - Remaining hours = 70 - current_cycle_used

2. **Pickup Phase**
   - Status: ON-DUTY (not driving)
   - Duration: 1 hour
   - Location: Pickup address

3. **Driving Phase** (Loop)
   - Check if cycle exceeded
   - If yes: Add 10-hour rest, reset cycle
   - Calculate drive distance (limited by 1000-mile fuel interval)
   - Check daily driving limits (11 hours max)
   - Add DRIVING log
   - Update remaining distance

4. **Fuel Stops**
   - After every 1,000 miles driven
   - Status: ON-DUTY (not driving)
   - Duration: 30 minutes
   - Location: "Fuel Stop"

5. **Dropoff Phase**
   - Status: ON-DUTY (not driving)
   - Duration: 1 hour
   - Location: Dropoff address

### Output
Array of ELDLog entries showing:
- Date
- Start and end times
- Status
- Location
- Miles driven

## Route Calculation

### Geocoding
Uses OpenStreetMap Nominatim API to convert location names to coordinates:
- Input: "San Francisco, CA"
- Output: (37.7749, -122.4194)

### Route Distance
Uses OSRM (Open Source Routing Machine) to calculate:
- Distance in miles
- Estimated duration in hours
- Route geometry (polyline)

## Frontend Components

### TripForm
- Input form for trip details
- Validation
- API call to backend

### RouteMap
- Leaflet map display
- Markers for current, pickup, dropoff
- Route information display

### ELDLogDisplay
- Timeline view of logs
- Log sheet export
- Compliance statistics

## Compliance Checks

The application automatically ensures:
1. ✅ No driving beyond 11-hour daily limit
2. ✅ Respects 70-hour/8-day cycle
3. ✅ Schedules mandatory rest breaks
4. ✅ Includes fuel stops every 1000 miles
5. ✅ Adds pickup/dropoff handling time
6. ✅ Generates chronological log entries

## API Endpoints

### Calculate Route & Generate Logs
```
POST /api/trips/calculate_route/

Success Response (201):
{
    "id": 1,
    "pickup_location": "San Francisco, CA",
    "dropoff_location": "Seattle, WA",
    "route_distance": 806.5,
    "estimated_duration": 12.3,
    "eld_logs": [...]
}

Error Response (400):
{
    "error": "Could not geocode all locations"
}
```

### Get All Trips
```
GET /api/trips/

Response:
[
    {
        "id": 1,
        "pickup_location": "San Francisco, CA",
        "dropoff_location": "Seattle, WA",
        "route_distance": 806.5,
        "created_at": "2024-01-15T09:00:00Z"
    }
]
```

## Performance Optimizations

1. **Caching**
   - Cache geocoding results
   - Cache frequently used routes

2. **Async Processing**
   - Consider async task queue for long calculations
   - Real-time notifications for completion

3. **Database**
   - Index on created_at and status fields
   - Bulk create for ELD logs

## Security Considerations

1. **Input Validation**
   - Validate location names (length, characters)
   - Validate numeric inputs (cycle hours: 0-70)

2. **Rate Limiting**
   - Limit API calls per user
   - Throttle external API calls

3. **HTTPS**
   - Always use HTTPS in production
   - Validate SSL certificates

4. **Environment Variables**
   - Never commit API keys
   - Use .env files for sensitive data

## Testing

### Unit Tests
```python
# Test ELD log generation
def test_eld_generation_with_long_trip():
    trip = Trip(
        route_distance=2000,
        current_cycle_used=10
    )
    generator = ELDLogGenerator(trip)
    logs = generator.generate_logs()
    assert any(log.status == 'OFF' for log in logs)  # Rest required
```

### Integration Tests
```python
# Test API endpoint
def test_calculate_route_endpoint():
    response = client.post('/api/trips/calculate_route/', {
        'current_location': 'LA, CA',
        'pickup_location': 'SF, CA',
        'dropoff_location': 'Seattle, WA'
    })
    assert response.status_code == 201
    assert response.data['route_distance'] > 0
```

## Future Enhancements

1. **Advanced Features**
   - Multiple driver support
   - Team assignments
   - Real-time location tracking
   - Predictive ETA

2. **Compliance**
   - Automatic violation detection
   - Alerts for exceeding limits
   - Audit trail for modifications

3. **Integration**
   - Fleet management systems
   - Telematics integration
   - Fuel card systems
   - Dispatch systems

4. **Mobile**
   - Native iOS/Android apps
   - Offline mode
   - Voice commands

## References

- FMCSA Hours of Service Rules: https://www.fmcsa.dot.gov/regulations/hours-of-service
- Part 395 Regulations: https://www.ecfr.gov/current/title-49/part-395
- ELD Rule: https://www.fmcsa.dot.gov/regulations/electronic-logging-device

## Support

For technical questions or issues, please refer to the README.md or create an issue on GitHub.
