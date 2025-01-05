import React, { useEffect } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { useHistory } from "react-router-dom";
import { auth, signInWithGoogle, db } from "../firebase";
import { doc, setDoc, getDoc } from "firebase/firestore";
import "./styles/Home.css";

function Home() {
  const [user, loading, error] = useAuthState(auth);
  const history = useHistory();

  useEffect(() => {
    if (loading) return;
    if (user) {
      // Check if the user already exists in the "users" collection
      const userRef = doc(db, "users", user.uid);
      getDoc(userRef).then((docSnapshot) => {
        if (!docSnapshot.exists()) {
          // If the user doesn't exist, create a new document in the "users" collection
          setDoc(userRef, {
            uid: user.uid,
            displayName: user.displayName,
            email: user.email,
            photoURL: user.photoURL,
            enrolledClassrooms: [], // Initialize an empty array for enrolled classrooms
          })
            .then(() => {
              console.log("User document created in Firestore");
            })
            .catch((error) => {
              console.error("Error creating user document: ", error);
            });
        }
      });

      // Redirect to the dashboard
      history.push("/dashboard");
    }
  }, [loading, user, history]);

  return (
    <div className="home" style={{ transform: "scale(0.6)" }}>
      <div className="home__container">
        <img
          src="./ministry.jpg"
          alt="Bharat Shiksha Image"
          className="home__image"
          style={{ transform: "scale(0.9)" }}
        />
        <button className="home__login" onClick={signInWithGoogle}>
          Login with Google
        </button>
      </div>
    </div>
  );
}

export default Home;