import React, { useState } from 'react';
import './App.css';
import TripForm from './components/TripForm';
import RouteMap from './components/RouteMap';
import ELDLogDisplay from './components/ELDLogDisplay';

function App() {
  const [tripData, setTripData] = useState(null);
  const [eldLogs, setEldLogs] = useState([]);

  const handleTripSubmit = (data) => {
    setTripData(data);
    setEldLogs(data.eld_logs || []);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🚛 ELD Trip Planner</h1>
        <p>Electronic Logging Device Trip Planning & HOS Compliance</p>
      </header>
      
      <div className="app-container">
        <div className="left-panel">
          <TripForm onTripSubmit={handleTripSubmit} />
        </div>
        
        <div className="right-panel">
          {tripData && (
            <>
              <RouteMap trip={tripData} />
              <ELDLogDisplay logs={eldLogs} trip={tripData} />
            </>
          )}
          {!tripData && (
            <div className="placeholder">
              <p>Enter trip details and click "Calculate Route" to view the map and ELD logs</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
