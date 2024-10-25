// src/components/Banner.jsx
import React, { useState, useEffect } from 'react';
import './Banner.css';
import a from '../images/dis-man1.jpg';
import b from '../images/dis-man2.jpg';
import c from '../images/dis-man3.jpg';
import News from './News'; // Import the News component

const images = [a, b, c]; // Array of images
const imageText = [
  "Disaster Management",
  "Slide 2 Description",
  "Slide 3 Description"
];

const Banner = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [backgroundImage, setBackgroundImage] = useState(images[0]);

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
  };

  useEffect(() => {
    const interval = setInterval(nextSlide, 4000);
    setBackgroundImage(images[currentIndex]);
    return () => clearInterval(interval);
  }, [currentIndex]);

  return (
    <div className="banner" style={{ backgroundImage: `url(${backgroundImage})` }}>
      <div className="banner-text">
        <h1>SAHYOG</h1>
        <p>{imageText[currentIndex]}</p>
      </div>
      <News /> {/* Add News section here */}
    </div>
  );
};

export default Banner;
