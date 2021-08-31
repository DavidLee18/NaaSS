// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { onAuthStateChanged, getAuth } from "firebase/auth";
import store from "../store";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDnIHhUCE6Oj4EB5GxZy7XkSxqPAOvF4KQ",
  authDomain: "naass-ba0cd.firebaseapp.com",
  projectId: "naass-ba0cd",
  storageBucket: "naass-ba0cd.appspot.com",
  messagingSenderId: "861793025868",
  appId: "1:861793025868:web:e384929c018d228567d9e9",
  measurementId: "G-EPWQHFT0M8"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// eslint-disable-next-line no-unused-vars
const analytics = getAnalytics(app);

onAuthStateChanged(getAuth(app), user => {
    if (user) {
        store.commit('login', user.uid);
    } else {
        store.commit('logout');
    }
});