import React, { useState } from 'react';

const VolunteerForm = () => {
  const [formData, setFormData] = useState({
    VolunteerName: '',
    VolunteerEmail: '',
    Gender: 'Male',
    Age: '',
    PlaceOfStay: '',
    LanguagesKnown: '',
    PreviousExperience: '',
    Height: '',
    Weight: '',
    EducationalQualification: '',
  });

  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Convert the number fields (Age, Height, and Weight) to actual numeric values
    const convertedFormData = {
      ...formData,
      Age: parseInt(formData.Age, 10),
      Height: parseFloat(formData.Height),
      Weight: parseFloat(formData.Weight),
    };

    // Basic form validation before submission
    if (!convertedFormData.VolunteerEmail || 
        !convertedFormData.VolunteerName || 
        convertedFormData.Age <= 0 || 
        convertedFormData.Height <= 0 || 
        convertedFormData.Weight <= 0) {
      setResponse({ error: 'Please fill out all required fields with valid data!' });
      return;
    }

    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/add_volunteer', {
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
    <div className="volunteer-form-container">
      <h2>Register as a Volunteer</h2>
      <form onSubmit={handleSubmit}>
        <input 
          name="VolunteerName" 
          value={formData.VolunteerName} 
          onChange={handleChange} 
          placeholder="Name" 
          required 
        />
        <input 
          name="VolunteerEmail" 
          type="email" 
          value={formData.VolunteerEmail} 
          onChange={handleChange} 
          placeholder="Email" 
          required 
        />
        <select 
          name="Gender" 
          value={formData.Gender} 
          onChange={handleChange} 
          required
        >
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
        <input 
          name="Age" 
          type="number" 
          value={formData.Age} 
          onChange={handleChange} 
          placeholder="Age" 
          min="0" 
          required 
        />
        <input 
          name="PlaceOfStay" 
          value={formData.PlaceOfStay} 
          onChange={handleChange} 
          placeholder="Place of Stay" 
          required 
        />
        <input 
          name="LanguagesKnown" 
          value={formData.LanguagesKnown} 
          onChange={handleChange} 
          placeholder="Languages Known" 
          required 
        />
        <textarea 
          name="PreviousExperience" 
          value={formData.PreviousExperience} 
          onChange={handleChange} 
          placeholder="Previous Experience"
        ></textarea>
        <input 
          name="Height" 
          type="number" 
          value={formData.Height} 
          onChange={handleChange} 
          placeholder="Height (m)" 
          min="0" 
          step="0.01"
          required 
        />
        <input 
          name="Weight" 
          type="number" 
          value={formData.Weight} 
          onChange={handleChange} 
          placeholder="Weight (kg)" 
          min="0" 
          step="0.1"
          required 
        />
        <input 
          name="EducationalQualification" 
          value={formData.EducationalQualification} 
          onChange={handleChange} 
          placeholder="Educational Qualification" 
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
            <p style={{ color: 'green' }}>Registered successfully! Your password is: {response.password}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default VolunteerForm;
