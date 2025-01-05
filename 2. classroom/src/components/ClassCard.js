import { IconButton } from "@material-ui/core";
import { AssignmentIndOutlined, FolderOpenOutlined } from "@material-ui/icons";
import React from "react";
import { useHistory } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faStar, faStarHalfAlt } from "@fortawesome/free-solid-svg-icons";
import { faStar as farStar } from "@fortawesome/free-regular-svg-icons";
import "./ClassCard.css";

function ClassCard({ name, creatorName, creatorPhoto, id, style }) {
  const history = useHistory();

  const goToClass = () => {
    history.push(`/class/${id}`);
  };

  // Function to generate a random rating between 3.5 and 5
  const generateRandomRating = () => {
    const min = 3.5;
    const max = 5;
    return Math.random() * (max - min) + min;
  };

  // Function to generate a random number of reviews between 50 and 500
  const generateRandomReviews = () => {
    const min = 50;
    const max = 500;
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };

  const rating = generateRandomRating();
  const reviews = generateRandomReviews();

  // Function to render stars based on the rating
  const renderStars = (rating) => {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 !== 0;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);

    return (
      <>
        {Array(fullStars).fill().map((_, i) => (
          <FontAwesomeIcon key={`full-${i}`} icon={faStar} className="animated" />
        ))}
        {halfStar && <FontAwesomeIcon key="half" icon={faStarHalfAlt} className="animated" />}
        {Array(emptyStars).fill().map((_, i) => (
          <FontAwesomeIcon key={`empty-${i}`} icon={farStar} className="animated" />
        ))}
      </>
    );
  };

  return (
    <div className="classCard" style={style} onClick={goToClass}>
      <div className="classCard__upper">
        <div className="classCard__className">{name}</div>
        <div className="classCard__creatorName">{creatorName}</div>
        <img src={creatorPhoto} className="classCard__creatorPhoto" alt={`${creatorName}'s photo`} />
      </div>
      <div className="classCard__middle">
        This course offers comprehensive content, practical exercises, and expert guidance to help you master the subject.
      </div>
      <div className="classCard__rating">
        {renderStars(rating)}
        <span>({reviews} reviews)</span>
      </div>
      <div className="classCard__lower">
        <IconButton>
          <FolderOpenOutlined />
        </IconButton>
        <IconButton>
          <AssignmentIndOutlined />
        </IconButton>
      </div>
    </div>
  );
}

export default ClassCard;