// UpdateCamp.jsx
import React, { useState } from 'react';
import './UpdateCamp.css';

const UpdateCamp = () => {
  const [formData, setFormData] = useState({
    CampName: '',
    Password: '',
    Capacity: '',
    VolunteerReq: '',
    VolunteerAvail: '',
    FundReq: '',
    FundAvail: '',
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
    setLoading(true);

    try {
      const res = await fetch(`http://localhost:5000/update_camp/${formData.CampName}/${formData.Password}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      setResponse(data.message);
    } catch (error) {
      setResponse('An error occurred during update.');
    }
    setLoading(false);
  };

  return (
    <div className="update-camp-container">
      <h2>Update Camp Details</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="CampName"
          value={formData.CampName}
          onChange={handleChange}
          placeholder="Camp Name"
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
          name="Capacity"
          type="number"
          value={formData.Capacity}
          onChange={handleChange}
          placeholder="Capacity"
          min="1"
        />
        <input
          name="VolunteerReq"
          type="number"
          value={formData.VolunteerReq}
          onChange={handleChange}
          placeholder="Volunteers Required"
          min="0"
        />
        <input
          name="VolunteerAvail"
          type="number"
          value={formData.VolunteerAvail}
          onChange={handleChange}
          placeholder="Volunteers Available"
          min="0"
        />
        <input
          name="FundReq"
          value={formData.FundReq}
          onChange={handleChange}
          placeholder="Fund Requirement"
        />
        <input
          name="FundAvail"
          value={formData.FundAvail}
          onChange={handleChange}
          placeholder="Available Funds"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Updating...' : 'Update'}
        </button>
      </form>

      {response && <p>{response}</p>}
    </div>
  );
};

export default UpdateCamp;
