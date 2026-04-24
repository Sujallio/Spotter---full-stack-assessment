import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import './RouteMap.css';

// Fix for default marker icons in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

function RouteMap({ trip }) {
  const pickupCoords = [trip.pickup_lat, trip.pickup_lng];
  const dropoffCoords = [trip.dropoff_lat, trip.dropoff_lng];
  const currentCoords = [trip.current_lat, trip.current_lng];

  const centerLat = (trip.pickup_lat + trip.dropoff_lat) / 2;
  const centerLng = (trip.pickup_lng + trip.dropoff_lng) / 2;

  return (
    <div className="map-container">
      <h2>📍 Route Map</h2>
      <div className="route-info">
        <div className="info-item">
          <span className="label">Distance:</span>
          <span className="value">{trip.route_distance?.toFixed(1)} miles</span>
        </div>
        <div className="info-item">
          <span className="label">Est. Duration:</span>
          <span className="value">{trip.estimated_duration?.toFixed(1)} hours</span>
        </div>
      </div>
      
      <MapContainer
        center={[centerLat, centerLng]}
        zoom={6}
        className="leaflet-map"
      >
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <Marker position={currentCoords}>
          <Popup>
            <div>
              <strong>Current Location</strong>
              <p>{trip.current_location}</p>
            </div>
          </Popup>
        </Marker>

        <Marker position={pickupCoords}>
          <Popup>
            <div>
              <strong>Pickup Location</strong>
              <p>{trip.pickup_location}</p>
            </div>
          </Popup>
        </Marker>

        <Marker position={dropoffCoords}>
          <Popup>
            <div>
              <strong>Dropoff Location</strong>
              <p>{trip.dropoff_location}</p>
            </div>
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}

export default RouteMap;
