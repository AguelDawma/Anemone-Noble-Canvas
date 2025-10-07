
// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-analytics.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

import { getAuth } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
apiKey: "AIzaSyBjsmY812lzY4JO6DTnh3UwOnTiIM4qsMY",
authDomain: "anemone-noble-canvas-website.firebaseapp.com",
projectId: "anemone-noble-canvas-website",
storageBucket: "anemone-noble-canvas-website.firebasestorage.app",
messagingSenderId: "80886795168",
appId: "1:80886795168:web:985ac7549c5ea6556572c5",
measurementId: "G-MZ847DEQNH"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

//get the auth and firestore instances
export const auth = getAuth(app);
export const db = getFirestore(app);