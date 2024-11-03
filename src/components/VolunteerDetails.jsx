import React, { useState } from 'react';
import axios from 'axios';
import './VolunteerDetails.css'

const VolunteerDetails = () => {
    const [location, setLocation] = useState('');
    const [license, setLicense] = useState(null);

    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append('location', location);
        formData.append('license', license);

        try {
            const response = await axios.post('http://localhost:5000/add_volunteer_details', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            if (response.data.success) {
                alert('Details submitted successfully!');
            }
        } catch (err) {
            alert('An error occurred while submitting your details. Please try again.');
        }
    };

    return (
        <div className="volunteer-details-container">
            <h2>Volunteer Details</h2>
            <input
                type="text"
                placeholder="Preferred Location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
            />
            <input
                type="file"
                onChange={(e) => setLicense(e.target.files[0])}
            />
            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
    
};

export default VolunteerDetails;
