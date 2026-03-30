import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: 'AIzaSyAmIcjDkVE8fcIVz-PCUbwnxjCNy3219KE',
  authDomain: 'civic-pulse-ffac8.firebaseapp.com',
  projectId: 'civic-pulse-ffac8',
  storageBucket: 'civic-pulse-ffac8.firebasestorage.app',
  messagingSenderId: '499580733822',
  appId: '1:499580733822:web:284b540d54b14315148b2f',
  measurementId: 'G-TSWT74SNJV',
}

const app = initializeApp(firebaseConfig)

export const auth = getAuth(app)
export const db = getFirestore(app)
export const googleProvider = new GoogleAuthProvider()
