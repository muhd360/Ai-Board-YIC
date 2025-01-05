import { IconButton, Button, Typography } from "@material-ui/core";
import { MoreVert, ThumbUp, Comment, Share } from "@material-ui/icons";
import React, { useState } from "react";
import "./Announcement.css";

function Announcement({ image, name, date, content, authorId }) {
  const [expanded, setExpanded] = useState(false);

  // Utility function to parse the date string into a JavaScript Date object
  const parseDateString = (dateString) => {
    const cleanedDateString = dateString
      .replace(/(\d+)(st|nd|rd|th)/, "$1") // Remove ordinal suffix (e.g., "5th" -> "5")
      .replace(/(\d{2})$/, "20$1"); // Convert "25" to "2025"
    return new Date(cleanedDateString);
  };

  // Check if the date string is valid
  const isValidDateString = (dateString) => {
    return dateString && !isNaN(parseDateString(dateString).getTime());
  };

  // Format the date in Indian style
  const formattedDate = isValidDateString(date)
    ? new Intl.DateTimeFormat("en-IN", {
        day: "numeric",
        month: "short",
        year: "numeric",
      }).format(parseDateString(date))
    : "N/A"; // Fallback for invalid or missing dates

  // Toggle content expansion
  const toggleExpand = () => {
    setExpanded(!expanded);
  };

  return (
    <div className="announcement">
      <div className="announcement__header">
        <div className="announcement__profile">
          <img src={image} alt="Profile" className="announcement__image" />
          <div className="announcement__profileInfo">
            <Typography variant="subtitle1" className="announcement__name">
              {name}
            </Typography>
            <Typography variant="caption" className="announcement__date">
              Posted on {formattedDate}
            </Typography>
          </div>
        </div>
        <IconButton className="announcement__moreButton">
          <MoreVert />
        </IconButton>
      </div>

      <div className="announcement__content">
        <Typography
          variant="body1"
          className={`announcement__text ${expanded ? "expanded" : ""}`}
        >
          {content}
        </Typography>
        {content.length > 200 && (
          <Button onClick={toggleExpand} className="announcement__readMore">
            {expanded ? "Read Less" : "Read More"}
          </Button>
        )}
      </div>

      <div className="announcement__footer">
        <Button startIcon={<ThumbUp />} className="announcement__actionButton">
          Like
        </Button>
        <Button startIcon={<Comment />} className="announcement__actionButton">
          Comment
        </Button>
        
      </div>
    </div>
  );
}

export default Announcement;