import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css';

const Register = () => {
  const navigate = useNavigate();

  // Function to handle navigation with a dynamic path
  const handleClick = (path) => {
    navigate(path); // Navigate to the provided path
  };

  return (
    <div className="register-page">
      <h1 className="register-title">Register</h1>
      <div className="register-boxes">
        <div className="register-box ngo" onClick={() => handleClick('/ngo')}>
          <h2>NGO</h2>
        </div>
        <div className="register-box donor" onClick={() => handleClick('/donor')}>
          <h2>Donor</h2>
        </div>
        <div className="register-box volunteer" onClick={() => handleClick('/volunteer')}>
          <h2>Volunteer</h2>
        </div>
        <div className="register-box camp" onClick={() => handleClick('/camp')}>
          <h2>Camp</h2>
        </div>
      </div>
    </div>
  );
};

export default Register;
