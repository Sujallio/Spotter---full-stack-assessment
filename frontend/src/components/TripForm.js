import React, { useState } from 'react';
import axios from 'axios';
import './TripForm.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function TripForm({ onTripSubmit }) {
  const [formData, setFormData] = useState({
    current_location: '',
    pickup_location: '',
    dropoff_location: '',
    current_cycle_used: 0,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_URL}/trips/calculate_route/`, {
        current_location: formData.current_location,
        pickup_location: formData.pickup_location,
        dropoff_location: formData.dropoff_location,
        current_cycle_used: parseFloat(formData.current_cycle_used),
      });

      onTripSubmit(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to calculate route. Please check your locations.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="trip-form" onSubmit={handleSubmit}>
      <h2>Trip Details</h2>

      {error && <div className="error">{error}</div>}

      <div className="form-group">
        <label htmlFor="current_location">Current Location *</label>
        <input
          type="text"
          id="current_location"
          name="current_location"
          placeholder="e.g., Los Angeles, CA"
          value={formData.current_location}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="pickup_location">Pickup Location *</label>
        <input
          type="text"
          id="pickup_location"
          name="pickup_location"
          placeholder="e.g., San Francisco, CA"
          value={formData.pickup_location}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="dropoff_location">Dropoff Location *</label>
        <input
          type="text"
          id="dropoff_location"
          name="dropoff_location"
          placeholder="e.g., Seattle, WA"
          value={formData.dropoff_location}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="current_cycle_used">Current Cycle Used (Hours)</label>
        <input
          type="number"
          id="current_cycle_used"
          name="current_cycle_used"
          placeholder="0"
          min="0"
          max="70"
          step="0.5"
          value={formData.current_cycle_used}
          onChange={handleChange}
        />
        <small>Enter hours already used in current 8-day cycle</small>
      </div>

      <button type="submit" className="btn" disabled={loading}>
        {loading ? '⏳ Calculating Route...' : '📍 Calculate Route'}
      </button>
    </form>
  );
}

export default TripForm;
