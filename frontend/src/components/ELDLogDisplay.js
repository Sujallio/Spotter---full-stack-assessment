import React, { useState, useRef, useEffect } from 'react';
import './ELDLogDisplay.css';

function ELDLogDisplay({ logs, trip }) {
  const [activeTab, setActiveTab] = useState('timeline');
  const canvasRef = useRef(null);

  const statusColors = {
    'OFF': '#e74c3c',
    'SB': '#3498db',
    'DRIVING': '#2ecc71',
    'ON': '#f39c12',
  };

  const statusLabels = {
    'OFF': 'Off Duty',
    'SB': 'Sleeper Berth',
    'DRIVING': 'Driving',
    'ON': 'On Duty',
  };

  useEffect(() => {
    if (activeTab === 'logsheet' && logs.length > 0) {
      drawLogSheet();
    }
  }, [activeTab, logs]);

  const drawLogSheet = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // White background
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, width, height);

    // Draw title
    ctx.fillStyle = '#333';
    ctx.font = 'bold 16px Arial';
    ctx.fillText('DRIVER VEHICLE INSPECTION REPORT', 20, 30);

    // Draw legend
    ctx.font = '12px Arial';
    let legendY = 50;
    const statusOrder = ['OFF', 'DRIVING', 'ON', 'SB'];
    statusOrder.forEach((status, idx) => {
      ctx.fillStyle = statusColors[status];
      ctx.fillRect(20, legendY + idx * 20, 15, 15);
      ctx.fillStyle = '#333';
      ctx.fillText(statusLabels[status], 40, legendY + idx * 20 + 12);
    });

    // Draw log entries as a timeline
    const entryHeight = 100;
    let yPos = 150;

    logs.slice(0, 5).forEach((log, idx) => {
      const startTime = new Date(log.start_time);
      const endTime = new Date(log.end_time);
      
      // Draw entry box
      ctx.strokeStyle = '#ccc';
      ctx.lineWidth = 1;
      ctx.strokeRect(20, yPos, width - 40, entryHeight);

      // Draw status color
      ctx.fillStyle = statusColors[log.status];
      ctx.fillRect(20, yPos, 5, entryHeight);

      // Draw text
      ctx.fillStyle = '#333';
      ctx.font = 'bold 12px Arial';
      ctx.fillText(`${statusLabels[log.status]}`, 35, yPos + 15);

      ctx.font = '11px Arial';
      ctx.fillText(`Time: ${startTime.toLocaleTimeString()} - ${endTime.toLocaleTimeString()}`, 35, yPos + 32);
      ctx.fillText(`Location: ${log.location}`, 35, yPos + 47);
      ctx.fillText(`Miles: ${log.miles_driven?.toFixed(1) || 0}`, 35, yPos + 62);

      yPos += entryHeight + 10;
    });

    // Draw footer
    ctx.fillStyle = '#666';
    ctx.font = '10px Arial';
    ctx.fillText(`Trip: ${trip.pickup_location} → ${trip.dropoff_location}`, 20, height - 10);
  };

  const totalDrivingHours = logs
    .filter(log => log.status === 'DRIVING')
    .reduce((sum, log) => {
      const start = new Date(log.start_time);
      const end = new Date(log.end_time);
      return sum + (end - start) / (1000 * 60 * 60);
    }, 0);

  const totalMiles = logs.reduce((sum, log) => sum + (log.miles_driven || 0), 0);

  return (
    <div className="eld-log-container">
      <h2>📋 Electronic Logging Device (ELD) Logs</h2>

      <div className="log-stats">
        <div className="stat-item">
          <span className="stat-label">Total Driving:</span>
          <span className="stat-value">{totalDrivingHours.toFixed(1)} hrs</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Total Miles:</span>
          <span className="stat-value">{totalMiles.toFixed(1)} mi</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Log Entries:</span>
          <span className="stat-value">{logs.length}</span>
        </div>
      </div>

      <div className="tab-buttons">
        <button
          className={`tab-btn ${activeTab === 'timeline' ? 'active' : ''}`}
          onClick={() => setActiveTab('timeline')}
        >
          Timeline
        </button>
        <button
          className={`tab-btn ${activeTab === 'logsheet' ? 'active' : ''}`}
          onClick={() => setActiveTab('logsheet')}
        >
          Log Sheet
        </button>
      </div>

      {activeTab === 'timeline' && (
        <div className="timeline-view">
          <div className="legend">
            {Object.entries(statusLabels).map(([status, label]) => (
              <div key={status} className="legend-item">
                <div
                  className="legend-color"
                  style={{ backgroundColor: statusColors[status] }}
                ></div>
                <span>{label}</span>
              </div>
            ))}
          </div>

          <div className="log-entries">
            {logs.length === 0 ? (
              <p className="no-logs">No ELD logs generated yet.</p>
            ) : (
              logs.map((log, idx) => {
                const startTime = new Date(log.start_time);
                const endTime = new Date(log.end_time);
                const duration = (endTime - startTime) / (1000 * 60 * 60);

                return (
                  <div
                    key={log.id}
                    className="log-entry"
                    style={{
                      borderLeftColor: statusColors[log.status],
                    }}
                  >
                    <div className="entry-header">
                      <span className="status-badge" style={{ backgroundColor: statusColors[log.status] }}>
                        {statusLabels[log.status]}
                      </span>
                      <span className="entry-time">
                        {startTime.toLocaleString()}
                      </span>
                    </div>
                    <div className="entry-details">
                      <div className="detail-row">
                        <span className="detail-label">Duration:</span>
                        <span className="detail-value">{duration.toFixed(2)} hours</span>
                      </div>
                      <div className="detail-row">
                        <span className="detail-label">Location:</span>
                        <span className="detail-value">{log.location}</span>
                      </div>
                      <div className="detail-row">
                        <span className="detail-label">Miles:</span>
                        <span className="detail-value">{log.miles_driven?.toFixed(1) || 0} mi</span>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      )}

      {activeTab === 'logsheet' && (
        <div className="logsheet-view">
          <canvas
            ref={canvasRef}
            width={900}
            height={1200}
            className="log-canvas"
          ></canvas>
        </div>
      )}
    </div>
  );
}

export default ELDLogDisplay;
