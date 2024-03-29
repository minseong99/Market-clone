import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
import { getStorage } from "firebase/storage";
import { getAuth } from "firebase/auth";

// TODO: Replace the following with your app's Firebase project configuration
// See: https://firebase.google.com/docs/web/learn-more#config-object
const firebaseConfig = {
  apiKey: "AIzaSyB9GUI0gJ2FH-E8hpRfXimrpDE4Czcrarw",
  authDomain: "carrot-market-b7d7b.firebaseapp.com",
  databaseURL:
    "https://carrot-market-b7d7b-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "carrot-market-b7d7b",
  storageBucket: "carrot-market-b7d7b.appspot.com",
  messagingSenderId: "603522085668",
  appId: "1:603522085668:web:01b4694f84ede07ddd39b1",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Realtime Database and get a reference to the service
const database = getDatabase(app);
const storage = getStorage(app);
const auth = getAuth(app);
