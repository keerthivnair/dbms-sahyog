import React, { useState } from 'react';
import './NgoRegistration.css'; // You can create a CSS file for styles

const NgoRegistration = () => {
    const [formData, setFormData] = useState({
        LicenseNumber: '',
        NGOName: '',
        ChairmanName: '',
        YearOfEstablishment: '',
        Email: '',
        PhoneNumber: '',
        AmountDonated: '',
        Priority: '',
        Volunteers: '',
    });
    const [message, setMessage] = useState('');
    const [password, setPassword] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const generateRandomPassword = () => {
        const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        let password = '';
        for (let i = 0; i < 8; i++) {
            password += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        return password;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const generatedPassword = generateRandomPassword();
        setPassword(generatedPassword);

        const response = await fetch('http://localhost:5000/add_ngo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ...formData, Password: generatedPassword }),
        });

        if (response.ok) {
            const data = await response.text();
            setMessage(`Successfully registered! Your email: ${formData.Email}, Password: ${generatedPassword}`);
        } else {
            const error = await response.text();
            setMessage(error);
        }
    };

    return (
        <div className="ngo-registration">
            <h2>NGO Registration</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="LicenseNumber" placeholder="License Number" onChange={handleChange} required />
                <input type="text" name="NGOName" placeholder="NGO Name" onChange={handleChange} required />
                <input type="text" name="ChairmanName" placeholder="Chairman Name" onChange={handleChange} required />
                <input type="number" name="YearOfEstablishment" placeholder="Year of Establishment" onChange={handleChange} required />
                <input type="email" name="Email" placeholder="Email" onChange={handleChange} required />
                <input type="text" name="PhoneNumber" placeholder="Phone Number" onChange={handleChange} required />
                <input type="number" name="AmountDonated" placeholder="Amount Donated" onChange={handleChange} required />
                <input type="number" name="Priority" placeholder="Priority" onChange={handleChange} required />
                <input type="number" name="Volunteers" placeholder="Volunteers" onChange={handleChange} required />
                <button type="submit">Register</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default NgoRegistration;
