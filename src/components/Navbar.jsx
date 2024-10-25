import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const [data, setData] = useState([]);
  const [showAboutPopup, setShowAboutPopup] = useState(false);

  const fetchData = async () => {
    try {
      const response = await fetch("http://localhost:5000/reports"); // Replace with your API URL
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="navbar">
      {" "}
      <ul>
        {" "}
        <li
          className="about-link-container"
          onMouseEnter={() => setShowAboutPopup(true)}
          onMouseLeave={() => setShowAboutPopup(false)}
        >
          {" "}
          <Link to="/about" className="about-link">
            About
          </Link>
          {" "}
        </li>
        {/* Add more navigation links here if needed */}     {" "}
      </ul>
      {" "}
      <div className="scrolling-text">
        {" "}
        {data.length > 0 ? (
          data.map((item, index) => (
            <span key={index} className="scroll-item">
              {item.ReportDetails} &nbsp; | &nbsp;            {" "}
            </span>
          ))
        ) : (
          <span>Loading...</span>
        )}
        {" "}
      </div>
      {/* About pop-up positioned on the side */}     {" "}
      {showAboutPopup && (
        <div className="about-side-popup">
          <h4>About Us</h4>         {" "}
          <p>
            Learn more about our mission to support disaster
            management across the globe...          {" "}
          </p>
          {" "}
          <Link to="/about" className="popup-link">
            Read More          {" "}
          </Link>
          {" "}
        </div>
      )}
      {" "}
    </div>
  );
};

export default Navbar;
