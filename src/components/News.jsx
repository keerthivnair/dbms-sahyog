// src/components/News.jsx
import React, { useState, useEffect } from 'react';
import './News.css'; // Create a corresponding CSS file for styling

const News = () => {
  const [news, setNews] = useState([]);
  const [scrollToTopVisible, setScrollToTopVisible] = useState(false); // State to track visibility of back to top button

  const fetchNews = async () => {
    try {
      const response = await fetch('https://api.reliefweb.int/v1/disasters?appname=rwint-user-0&profile=list&preset=latest&slim=1&query%5Bvalue%5D=country.id%3A119&query%5Boperator%5D=AND');
      const result = await response.json();

      if (result.data) {
        // Sort the fetched news based on some criteria if necessary
        const fetchedNews = result.data.map(item => ({
          id: item.id,
          title: item.fields.name, // The disaster name
          status: item.fields.status, // The status of the disaster
          glide: item.fields.glide, // The glide code
          country: item.fields.country[0]?.name // The first country name
        }));

        // Sort news by relevance if applicable (You can modify the criteria)
        fetchedNews.sort((a, b) => new Date(b.glide) - new Date(a.glide)); // Example sort based on date
        setNews(fetchedNews);
      } else {
        console.error("No data found in the API response.");
        setNews([]); // Clear existing data if none found
      }
    } catch (error) {
      console.error("Error fetching news:", error);
    }
  };

  useEffect(() => {
    fetchNews();

    // Handle scroll events to show/hide the button
    const handleScroll = () => {
      if (window.scrollY > 200) {
        setScrollToTopVisible(true);
      } else {
        setScrollToTopVisible(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  return (
    <div className="news-section">
      <h2>Latest Disaster News</h2>
      <div className="news-cards-container">
        {news.length > 0 ? (
          news.map((item) => (
            <div key={item.id} className="news-card">
              <h4>{item.title}</h4>
              <p>Status: {item.status}</p>
              <p>Country: {item.country}</p>
              <p>GLIDE Code: {item.glide}</p>
            </div>
          ))
        ) : (
          <div className="loading">Loading news...</div>
        )}
      </div>

      {/* Back to Top Button */}
      {scrollToTopVisible && (
        <button className="back-to-top" onClick={scrollToTop}>
          ↑ Back to Top
        </button>
      )}
    </div>
  );
};

export default News;
