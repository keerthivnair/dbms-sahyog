// CampOptions.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './CampOptions.css';

const CampOptions = () => {
  const navigate = useNavigate();

  return (
    <div className="camp-options-container">
      <h2>Camp Options</h2>
      <div className="options">
        <button onClick={() => navigate('/update-camp')}>Update Camp Details</button>
        <button onClick={() => navigate('/other-action')}>Other Actions</button>
      </div>
    </div>
  );
};

export default CampOptions;
