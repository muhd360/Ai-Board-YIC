import React, { useEffect, useState } from "react";
import "./styles/Dashboard.css";
import { useAuthState } from "react-firebase-hooks/auth";
import { auth, db } from "../firebase";
import { useHistory } from "react-router-dom";
import ClassCard from "../components/ClassCard";
import { doc, onSnapshot } from "firebase/firestore";
import { CircularProgress, Button, Typography, TextField, Grid } from "@material-ui/core";

function Dashboard() {
  const [user, loading, error] = useAuthState(auth);
  const [classes, setClasses] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const history = useHistory();

  useEffect(() => {
    if (loading) return;
    if (!user) history.replace("/");
  }, [user, loading, history]);

  useEffect(() => {
    if (loading || !user) return;

    // Fetch the user's document from the "users" collection
    const userRef = doc(db, "users", user.uid);
    const unsubscribe = onSnapshot(
      userRef,
      (doc) => {
        if (doc.exists()) {
          const userData = doc.data();
          console.log("User Data:", userData); // Debugging: Log user data
          setClasses(userData.enrolledClassrooms || []);
        } else {
          console.log("No user document found!"); // Debugging: Log if no user document is found
          setClasses([]);
        }
      },
      (error) => {
        console.error("Error fetching user data: ", error);
      }
    );

    return () => unsubscribe();
  }, [user, loading]);

  // Filter classes based on search query
  const filteredClasses = classes.filter((individualClass) =>
    individualClass.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <div className="dashboard__loading">
        <CircularProgress />
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard__error">
        <Typography variant="h6" color="error">
          Error: {error.message}
        </Typography>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard__header">
        <Typography variant="h4" className="dashboard__title">
          My Classes
        </Typography>
        <TextField
          label="Search Classes"
          variant="outlined"
          size="small"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="dashboard__search"
        />
      </div>

      {filteredClasses.length === 0 ? (
        <div className="dashboard__empty">
          <Typography variant="h6" className="dashboard__emptyText">
            No classes found! Join or create one!
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => history.push("/create-class")}
          >
            Create Class
          </Button>
        </div>
      ) : (
        <Grid container className="dashboard__classContainer">
          {filteredClasses.map((individualClass) => (
            <Grid item key={individualClass.id} xs={12} sm={6} md={4} lg={3}>
              <ClassCard
                creatorName={individualClass.creatorName}
                creatorPhoto={individualClass.creatorPhoto}
                name={individualClass.name}
                id={individualClass.id}
              />
            </Grid>
          ))}
        </Grid>
      )}
    </div>
  );
}

export default Dashboard;