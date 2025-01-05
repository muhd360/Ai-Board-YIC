import React, { useState, useEffect } from 'react'; // Add useEffect
import { useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import { FaFilePdf, FaVideo, FaSun, FaMoon } from 'react-icons/fa'; // Icons
import { RotateSpinner } from 'react-spinners-kit'; // Loading spinner
import '../styles/ResourcePage.css'; // Import a CSS file for styling

function ResourcePage() {
  const { lectureNumber } = useParams();
  const [showTranscript, setShowTranscript] = useState(false);
  const [showSummary, setShowSummary] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Apply dark mode to the body element
  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [isDarkMode]);

  const videoPath = `../data/lec${lectureNumber}/lec${lectureNumber}.mp4`;
  const transcriptPath = `../data/lec${lectureNumber}/lec${lectureNumber}_transcript.pdf#toolbar=0&view=FitH`;
  const summaryPath = `../data/lec${lectureNumber}/lec${lectureNumber}_summary.pdf#toolbar=0&view=FitH`;

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  const handlePdfLoad = () => {
    setIsLoading(false);
  };

  const handleToggleTranscript = () => {
    if (!showTranscript) {
      setIsLoading(true); // Show spinner only when showing the transcript
    } else {
      setIsLoading(false); // Hide spinner when hiding the transcript
    }
    setShowTranscript(!showTranscript);
  };

  const handleToggleSummary = () => {
    if (!showSummary) {
      setIsLoading(true); // Show spinner only when showing the summary
    } else {
      setIsLoading(false); // Hide spinner when hiding the summary
    }
    setShowSummary(!showSummary);
  };

  return (
    <div className="resource-page">
      <Navbar />
      <div className="dark-mode-toggle" onClick={toggleDarkMode}>
        {isDarkMode ? <FaSun size={24} /> : <FaMoon size={24} />}
      </div>
      <h2>{`Lecture ${lectureNumber} Resources`}</h2>

      {/* Video Section */}
      <div className="video-section">
        <video src={videoPath} controls width="100%" height="auto">
          Your browser does not support the video tag.
        </video>
      </div>

      {/* Buttons for Transcript and Summary */}
      <div className="button-container">
        <button
          className="toggle-button"
          onClick={handleToggleTranscript}
          title="Toggle Transcript"
        >
          <FaFilePdf /> {showTranscript ? 'Hide Transcript' : 'Show Transcript'}
        </button>
        <button
          className="toggle-button"
          onClick={handleToggleSummary}
          title="Toggle Summary"
        >
          <FaFilePdf /> {showSummary ? 'Hide Summary' : 'Show Summary'}
        </button>
      </div>

      {/* Loading Spinner */}
      {isLoading && (
        <div className="loading-spinner">
          <RotateSpinner size={50} color="#007bff" />
        </div>
      )}

      {/* Transcript and Summary Sections (Side by Side) */}
      {(showTranscript || showSummary) && (
        <div className="pdf-container">
          {showTranscript && (
            <div className="pdf-section">
              <h3>Transcript</h3>
              <iframe
                src={transcriptPath}
                width="100%"
                height="100%"
                style={{ border: 'none', minHeight: '80vh' }}
                onLoad={handlePdfLoad}
              >
                <p>Your browser does not support PDFs. Please download the transcript to view it.</p>
              </iframe>
            </div>
          )}
          {showSummary && (
            <div className="pdf-section">
              <h3>Summary</h3>
              <iframe
                src={summaryPath}
                width="100%"
                height="100%"
                style={{ border: 'none', minHeight: '80vh' }}
                onLoad={handlePdfLoad}
              >
                <p>Your browser does not support PDFs. Please download the summary to view it.</p>
              </iframe>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ResourcePage;