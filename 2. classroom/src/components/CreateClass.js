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
import { createDialogAtom } from "../utils/atoms";
import { addDoc, collection, doc, updateDoc, arrayUnion } from "firebase/firestore";

function CreateClass() {
  const [user, loading, error] = useAuthState(auth);
  const [open, setOpen] = useRecoilState(createDialogAtom);
  const [className, setClassName] = useState("");

  const handleClose = () => {
    setOpen(false);
  };

  const createClass = async () => {
    if (!className.trim()) {
      alert("Please enter a class name.");
      return;
    }

    try {
      // Step 1: Create a new class in the "classes" collection
      const newClassRef = await addDoc(collection(db, "classes"), {
        creatorUid: user.uid,
        name: className,
        creatorName: user.displayName,
        creatorPhoto: user.photoURL,
        posts: [],
      });

      // Step 2: Add the class to the creator's "enrolledClassrooms" array in the "users" collection
      const userRef = doc(db, "users", user.uid);
      await updateDoc(userRef, {
        enrolledClassrooms: arrayUnion({
          id: newClassRef.id,
          name: className,
          creatorName: user.displayName,
          creatorPhoto: user.photoURL,
        }),
      });

      handleClose();
      alert("Classroom created successfully!");
      setClassName(""); // Clear the input field
    } catch (err) {
      console.error("Error creating class: ", err);
      alert(`Cannot create class - ${err.message}`);
    }
  };

  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="form-dialog-title"
      >
        <DialogTitle id="form-dialog-title">Create class</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Enter the name of the class, and we will create a classroom for you!
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            label="Class Name"
            type="text"
            fullWidth
            value={className}
            onChange={(e) => setClassName(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={createClass} color="primary">
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default CreateClass;