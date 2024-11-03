// NGORegistration.js
import React, { useState } from 'react';
import axios from 'axios';
import './NgoRegistration.css';

const NGORegistration = () => {
    const [licenseNumber, setLicenseNumber] = useState('');
    const [ngoName, setNgoName] = useState('');
    const [chairmanName, setChairmanName] = useState('');
    const [yearOfEstablishment, setYearOfEstablishment] = useState('');
    const [email, setEmail] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [isVerified, setIsVerified] = useState(false);
    const [showRegistrationForm, setShowRegistrationForm] = useState(false);
    const [message, setMessage] = useState('');

    // Function to verify NGO
    const verifyNGO = async () => {
        try {
            const response = await axios.post('/verify_ngo', { licenseNumber });
            setMessage(response.data.message);
            if (response.data.verified) {
                setIsVerified(true);
            }
        } catch (error) {
            setMessage('Verification failed. Please check the NGO name and license number.');
        }
    };

    // Function to submit the complete NGO registration form
    const submitNGOForm = async () => {
        try {
            const data = { ngoName, licenseNumber, chairmanName, yearOfEstablishment, email, phoneNumber };
            const response = await axios.post('/add_ngo', data);
            setMessage(response.data.message);
        } catch (error) {
            setMessage('Error in NGO registration.');
        }
    };

    return (
        <div className="ngo-registration-container">
            <h2 className="ngo-registration-title">NGO Registration</h2>

            {message && <p className="ngo-registration-message">{message}</p>}

            {/* Initial NGO Verification Form */}
            <form className="ngo-verification-form">
                <label className="form-label">
                    NGO Name:
                    <input
                        className="form-input"
                        type="text"
                        value={ngoName}
                        onChange={(e) => setNgoName(e.target.value)}
                        required
                    />
                </label>
                <label className="form-label">
                    License Number:
                    <input
                        className="form-input"
                        type="text"
                        value={licenseNumber}
                        onChange={(e) => setLicenseNumber(e.target.value)}
                        required
                    />
                </label>
                <button className="form-button" type="button" onClick={verifyNGO}>
                    Verify
                </button>
            </form>

            {/* Show button to reveal full form if verification is successful */}
            {isVerified && (
                <div className="proceed-button-container">
                    <button className="form-button" onClick={() => setShowRegistrationForm(true)}>
                        Proceed to Full Registration
                    </button>
                </div>
            )}

            {/* Additional Registration Form (Hidden initially) */}
            {showRegistrationForm && (
                <form className="ngo-full-registration-form">
                    <label className="form-label">
                        Chairman Name:
                        <input
                            className="form-input"
                            type="text"
                            value={chairmanName}
                            onChange={(e) => setChairmanName(e.target.value)}
                            required
                        />
                    </label>
                    <label className="form-label">
                        Year of Establishment:
                        <input
                            className="form-input"
                            type="number"
                            value={yearOfEstablishment}
                            onChange={(e) => setYearOfEstablishment(e.target.value)}
                            required
                        />
                    </label>
                    <label className="form-label">
                        Email:
                        <input
                            className="form-input"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </label>
                    <label className="form-label">
                        Phone Number:
                        <input
                            className="form-input"
                            type="text"
                            value={phoneNumber}
                            onChange={(e) => setPhoneNumber(e.target.value)}
                            required
                        />
                    </label>
                    <button className="form-button" type="button" onClick={submitNGOForm}>
                        Submit
                    </button>
                </form>
            )}
        </div>
    );
};

export default NGORegistration;
