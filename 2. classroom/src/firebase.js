import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from 'firebase/auth';
import { getFirestore, collection, query, where, getDocs, addDoc } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: "AIzaSyBTGKC6qzr4bruZmE0WcOJGSutqCD9hwj4",
  authDomain: "smartboardyic.firebaseapp.com",
  projectId: "smartboardyic",
  storageBucket: "smartboardyic.firebasestorage.app",
  messagingSenderId: "713904724685",
  appId: "1:713904724685:web:08fc280bdbe5fcf94e6784",
  measurementId: "G-8XJBJ0N52Q"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);
const googleProvider = new GoogleAuthProvider();

const signInWithGoogle = async () => {
  try {
    const response = await signInWithPopup(auth,googleProvider);
    console.log(response.user);
    const user = response.user;
    console.log(`User ID - ${user.uid}`);

     // Query Firestore for existing user
     const userQuery = query(
      collection(db, "users"),
      where("uid", "==", user.uid)
    );
    
    const querySnapshot = await getDocs(userQuery);

    if (querySnapshot.empty) {
      // Create a new user if none exists
      await addDoc(collection(db, "users"), {
        uid: user.uid,
        enrolledClassrooms: [],
      });
    }
  } catch (err) {
    alert(err.message);
  }
};
const logout = () => {
  auth.signOut();
};

export { app, auth, db, signInWithGoogle, logout };
