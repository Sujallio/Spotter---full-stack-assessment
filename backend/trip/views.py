from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Trip, ELDLog
from .serializers import TripSerializer, ELDLogSerializer
from .utils import RouteCalculator, ELDLogGenerator


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    
    @action(detail=False, methods=['post'])
    def calculate_route(self, request):
        """Calculate route and generate ELD logs"""
        try:
            current_location = request.data.get('current_location')
            pickup_location = request.data.get('pickup_location')
            dropoff_location = request.data.get('dropoff_location')
            current_cycle_used = float(request.data.get('current_cycle_used', 0))
            
            if not all([current_location, pickup_location, dropoff_location]):
                return Response(
                    {'error': 'Missing required fields'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Geocode locations
            current_coords = RouteCalculator.geocode_location(current_location)
            pickup_coords = RouteCalculator.geocode_location(pickup_location)
            dropoff_coords = RouteCalculator.geocode_location(dropoff_location)
            
            if not all([current_coords[0], pickup_coords[0], dropoff_coords[0]]):
                return Response(
                    {'error': 'Could not geocode all locations'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate route from pickup to dropoff
            route_data = RouteCalculator.calculate_route(pickup_coords, dropoff_coords)
            
            if not route_data:
                return Response(
                    {'error': 'Could not calculate route'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create trip
            trip = Trip.objects.create(
                current_location=current_location,
                current_lat=current_coords[0],
                current_lng=current_coords[1],
                pickup_location=pickup_location,
                pickup_lat=pickup_coords[0],
                pickup_lng=pickup_coords[1],
                dropoff_location=dropoff_location,
                dropoff_lat=dropoff_coords[0],
                dropoff_lng=dropoff_coords[1],
                current_cycle_used=current_cycle_used,
                route_distance=route_data['distance'],
                estimated_duration=route_data['duration']
            )
            
            # Generate ELD logs
            eld_generator = ELDLogGenerator(trip)
            eld_generator.generate_logs()
            
            serializer = TripSerializer(trip)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def eld_logs(self, request, pk=None):
        """Get ELD logs for a trip"""
        trip = self.get_object()
        logs = trip.eld_logs.all()
        serializer = ELDLogSerializer(logs, many=True)
        return Response(serializer.data)


class ELDLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ELDLog.objects.all()
    serializer_class = ELDLogSerializer
