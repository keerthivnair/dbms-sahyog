import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = () => {
  const navigate = useNavigate();

  // Function to handle navigation with a dynamic path
  const handleClick = (path) => {
    navigate(path); // Navigate to the provided path
  };

  return (
    <div className="login-page">
      <h1 className="login-title">Login</h1>
      <div className="login-boxes">
        <div className="login-box ngo" onClick={() => handleClick('/ngo-login')}>
          <h2>NGO</h2>
        </div>
        <div className="login-box donor" onClick={() => handleClick('/donor-login')}>
          <h2>Donor</h2>
        </div>
        <div className="login-box volunteer" onClick={() => handleClick('/volunteer-login')}>
          <h2>Volunteer</h2>
        </div>
        <div className="login-box camp" onClick={() => handleClick('/camp-login')}>
          <h2>Camp</h2>
        </div>
      </div>
    </div>
  );
};

export default Login;
