import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Camplogin.css';

const CampLogin = () => {
  const [formData, setFormData] = useState({
    CampName: '',
    Password: '',
  });
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

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
      const res = await fetch(`http://localhost:5000/get_camp/${formData.CampName}/${formData.Password}`, {
        method: 'POST',
      });

      const data = await res.json();
      if (res.ok) {
        // Successfully logged in
        navigate('/camp-options', { state: { camp: data } });
      } else {
        // Login failed
        setResponse(data.message);
      }
    } catch (error) {
      setResponse('An error occurred during login.');
    }
    setLoading(false);
  };

  return (
    <div className="login-camp-container">
      <h2>Camp Login</h2>
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
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>

      {response && <p style={{ color: 'red' }}>{response}</p>}
    </div>
  );
};

export default CampLogin;
