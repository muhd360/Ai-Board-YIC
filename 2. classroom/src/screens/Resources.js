import React from 'react';
import ResourceCard from './resourcescomponent/ResourceCard';
import Navbar from '../components/Navbar';
import "./styles/Resources.css";

function Resources() {
  const numberOfLectures = 5;

  const createArray = (length) => Array.from({ length }, (_, i) => i + 1);

  return (
    <>
      <Navbar />
      <div className="resources-page">
        <h1 className="resources-title">Explore Resources</h1>
        <div className="resources-container">
          {createArray(numberOfLectures).map((lectureNumber) => (
            <ResourceCard key={lectureNumber} lectureNumber={lectureNumber} />
          ))}
        </div>
      </div>
    </>
  );
}

export default Resources;
