import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App'; // Ensure App.jsx is correctly referenced
import './index.css';    // Optional, if you have global styles

// Create the root element to render your app
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
