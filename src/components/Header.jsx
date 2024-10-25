import React from 'react';
import './Header.css';
import logo from '../images/logo.jpeg'
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="header">
      <div className="logo">
        <img src={logo} alt="Govt Logo" />
        <span>Sahyog, Disaster Management Portal</span>
      </div>
      <div className="user-access">
        <a href="/login" className="login-link">Login</a>
        <Link to="/register" className="header-link">Register</Link>
      </div>
    </header>
  );
};

export default Header;
