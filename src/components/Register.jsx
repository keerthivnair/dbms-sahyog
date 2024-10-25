import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import './Register.css'; // Create a corresponding CSS file for styling


const Register = () => {
  const navigate = useNavigate(); // Initialize useNavigate

  const handleVolunteerClick = () => {
    navigate('/volunteer'); // Redirect to Volunteer form
  };

  return (
    <div className="register-page">
      <h1 className="register-title">Register</h1>
      <div className="register-boxes">
        <div className="register-box ngo">
          <h2>NGO</h2>
        </div>
        <div className="register-box donor">
          <h2>Donor</h2>
        </div>
        <div className="register-box volunteer" onClick={handleVolunteerClick}> {/* Add onClick handler */}
          <h2>Volunteer</h2>
        </div>
        <div className="register-box camp">
          <h2>Camp</h2>
        </div>
      </div>
    </div>
  );
};

export default Register;
