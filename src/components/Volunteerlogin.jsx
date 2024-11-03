import React, { useState } from 'react';
import axios from 'axios';
import "./Volunteerlogin.css"

const VolunteerLogin = ({ navigate }) => {
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async () => {
        try {
            const response = await axios.post('http://localhost:5000/volunteer_login', { name, password });
            if (response.data.success) {
                alert('Login successful!');
                navigate('/volunteer-details'); 
            } else {
                setError('Invalid name or password. Please try again or register if not yet done.');
            }
        } catch (err) {
            setError('An error occurred. Please try again later.');
        }
    };

    return (
        <div className="volunteer-login-container">
            <h2>Volunteer Login</h2>
            {error && <p>{error}</p>}
            <input
                type="text"
                placeholder="Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleLogin}>Login</button>
        </div>
    );
    
};

export default VolunteerLogin;
