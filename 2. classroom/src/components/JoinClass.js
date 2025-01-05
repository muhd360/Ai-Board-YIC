import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField,
} from "@material-ui/core";
import React, { useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { useRecoilState } from "recoil";
import { auth, db } from "../firebase";
import { joinDialogAtom } from "../utils/atoms";
import { doc, getDoc, updateDoc, arrayUnion } from "firebase/firestore";

function JoinClass() {
  const [open, setOpen] = useRecoilState(joinDialogAtom);
  const [user, loading, error] = useAuthState(auth);
  const [classId, setClassId] = useState("");

  const handleClose = () => {
    setOpen(false);
  };

  const joinClass = async () => {
    if (!classId.trim()) {
      alert("Please enter a class ID.");
      return;
    }

    try {
      // Check if the class exists
      const classRef = doc(db, "classes", classId);
      const classSnapshot = await getDoc(classRef);

      if (!classSnapshot.exists()) {
        alert("Class does not exist!");
        return;
      }

      const classData = classSnapshot.data();

      // Add the class to the user's enrolledClassrooms array
      const userRef = doc(db, "users", user.uid);
      await updateDoc(userRef, {
        enrolledClassrooms: arrayUnion({
          id: classId,
          name: classData.name,
          creatorName: classData.creatorName,
          creatorPhoto: classData.creatorPhoto,
        }),
      });

      alert(`Enrolled in ${classData.name} successfully!`);
      handleClose();
    } catch (err) {
      console.error("Error joining class: ", err);
      alert(`Cannot join class - ${err.message}`);
    }
  };

  return (
    <div className="joinClass">
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="form-dialog-title"
      >
        <DialogTitle id="form-dialog-title">Join class</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Enter the ID of the class to join the classroom.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            label="Class ID"
            type="text"
            fullWidth
            value={classId}
            onChange={(e) => setClassId(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={joinClass} color="primary">
            Join
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default JoinClass;