import React from 'react';
import { useHistory } from 'react-router-dom'; // Use useHistory instead of useNavigate
import "../styles/Resources.css";

function ResourceCard({ lectureNumber }) {
  const history = useHistory(); // Initialize the history object

  // Function to handle card click
  const handleCardClick = () => {
    history.push(`/resources/${lectureNumber}`); // Navigate to the respective lecture page
  };

  return (
    <div className="resource-card" onClick={handleCardClick} style={{ cursor: 'pointer' }}>
      <div className="resource-card-icon">📘</div>
      <h2 className="resource-card-title">Lecture {lectureNumber}</h2>
      <p className="resource-card-subtitle">Subtitle for Lecture {lectureNumber}</p>
      <p className="resource-card-description">
        Dive into exciting topics covered in Lecture {lectureNumber}. This lecture covers advanced concepts in programming, data structures, and algorithms.
      </p>
      <p className="resource-card-additional-info">
        Published on: January 5, 2025 | Author: Dr. John Doe
      </p>
      <button className="resource-card-btn">Explore</button>
    </div>
  );
}

export default ResourceCard;