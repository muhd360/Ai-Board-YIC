import { IconButton } from "@material-ui/core";
import { SendOutlined } from "@material-ui/icons";
import moment from "moment";
import React, { useEffect, useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { useHistory, useParams } from "react-router-dom";
import Announcement from "../components/Announcement";
import { auth, db } from "../firebase";
import { doc, onSnapshot, updateDoc, getDoc } from "firebase/firestore";
import "./styles/Class.css";

function Class() {
  const [classData, setClassData] = useState({});
  const [announcementContent, setAnnouncementContent] = useState("");
  const [posts, setPosts] = useState([]);
  const [user, loading, error] = useAuthState(auth);
  const { id } = useParams();
  const history = useHistory();

  // Update posts when classData changes
  useEffect(() => {
    if (classData?.posts) {
      // Create a new reversed array to avoid mutating the state directly
      const reversedArray = [...classData.posts].reverse();
      setPosts(reversedArray);
    }
  }, [classData]);

  // Create a new post
  const createPost = async () => {
    if (!announcementContent.trim()) {
      alert("Please enter some content for the announcement.");
      return;
    }

    try {
      const classRef = doc(db, "classes", id);
      const classSnapshot = await getDoc(classRef);

      if (!classSnapshot.exists()) {
        alert("Class does not exist!");
        return;
      }

      const classData = classSnapshot.data();
      const updatedPosts = [
        ...classData.posts,
        {
          authorId: user.uid,
          content: announcementContent,
          date: moment().format("MMM Do YY"),
          image: user.photoURL,
          name: user.displayName,
        },
      ];

      // Update the Firestore document
      await updateDoc(classRef, { posts: updatedPosts });

      // Clear the input field
      setAnnouncementContent("");
    } catch (error) {
      console.error("Error creating post: ", error);
      alert("There was an error posting the announcement. Please try again!");
    }
  };

  // Fetch class data in real-time
  useEffect(() => {
    if (!id) return;

    const classRef = doc(db, "classes", id);
    const unsubscribe = onSnapshot(
      classRef,
      (snapshot) => {
        if (!snapshot.exists()) {
          history.replace("/");
          return;
        }
        setClassData(snapshot.data());
      },
      (error) => {
        console.error("Error fetching class data: ", error);
      }
    );

    return () => unsubscribe();
  }, [id, history]);

  // Redirect if user is not logged in
  useEffect(() => {
    if (loading) return;
    if (!user) history.replace("/");
  }, [loading, user, history]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div className="class">
      <div className="class__nameBox">
        <div className="class__name">{classData?.name}</div>
      </div>
      <div className="class__announce">
        <img src={user?.photoURL} alt="User" />
        <input
          type="text"
          value={announcementContent}
          onChange={(e) => setAnnouncementContent(e.target.value)}
          placeholder="Announce something to your class"
        />
        <IconButton onClick={createPost}>
          <SendOutlined />
        </IconButton>
      </div>
      {posts?.map((post, index) => (
        <Announcement
          key={index} 
          authorId={post.authorId}
          content={post.content}
          date={post.date}
          image={post.image}
          name={post.name}
        />
      ))}
    </div>
  );
}

export default Class;