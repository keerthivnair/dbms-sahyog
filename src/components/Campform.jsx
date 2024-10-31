import React, { useState } from 'react';
import './Campform.css'

const CampForm = () => {
  const [formData, setFormData] = useState({
    CampName: '',
    Capacity: '',
    VolunteerReq: '',
    VolunteerAvail: '',
    FundReq: '',
    FundAvail: '',
    Password: '',
    Location: '',
  });

  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((formData) => ({
      ...formData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    
    const convertedFormData = {
      ...formData,
      Capacity: parseInt(formData.Capacity, 10),
      VolunteerReq: parseInt(formData.VolunteerReq, 10),
      VolunteerAvail: parseInt(formData.VolunteerAvail, 10),
      FundReq: formData.FundReq,
      FundAvail: formData.FundAvail,
    };

    // Basic form validation
    if (
      !convertedFormData.CampName ||
      !convertedFormData.Password ||
      !convertedFormData.Location ||
      convertedFormData.Capacity <= 0 ||
      convertedFormData.VolunteerReq < 0 ||
      convertedFormData.VolunteerAvail < 0
    ) {
      setResponse({ error: 'Please fill out all required fields with valid data!' });
      return;
    }

    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/add_camp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(convertedFormData),
      });

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      setResponse({ error: 'An error occurred during submission.' });
    }
    setLoading(false);
  };

  return (
    <div className="camp-form-container">
      <h2>Register a Camp</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="CampName"
          value={formData.CampName}
          onChange={handleChange}
          placeholder="Camp Name"
          required
        />
        <input
          name="Capacity"
          type="number"
          value={formData.Capacity}
          onChange={handleChange}
          placeholder="Capacity"
          min="1"
          required
        />
        <input
          name="VolunteerReq"
          type="number"
          value={formData.VolunteerReq}
          onChange={handleChange}
          placeholder="Volunteers Required"
          min="0"
          required
        />
        <input
          name="VolunteerAvail"
          type="number"
          value={formData.VolunteerAvail}
          onChange={handleChange}
          placeholder="Volunteers Available"
          min="0"
          required
        />
        <input
          name="FundReq"
          value={formData.FundReq}
          onChange={handleChange}
          placeholder="Fund Requirement"
          required
        />
        <input
          name="FundAvail"
          value={formData.FundAvail}
          onChange={handleChange}
          placeholder="Available Funds"
          required
        />
        <input
          name="Password"
          type="password"
          value={formData.Password}
          onChange={handleChange}
          placeholder="Password"
          required
        />
        <input
          name="Location"
          value={formData.Location}
          onChange={handleChange}
          placeholder="Location"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Register'}
        </button>
      </form>

      {response && (
        <div>
          {response.error ? (
            <p style={{ color: 'red' }}>{response.error}</p>
          ) : (
            <p style={{ color: 'green' }}>Camp registered successfully!</p>
          )}
        </div>
      )}
    </div>
  );
};

export default CampForm;
