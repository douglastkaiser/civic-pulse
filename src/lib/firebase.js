import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider, connectAuthEmulator } from 'firebase/auth'
import { getFirestore, connectFirestoreEmulator } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || 'AIzaSyAmIcjDkVE8fcIVz-PCUbwnxjCNy3219KE',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || 'civic-pulse-ffac8.firebaseapp.com',
  projectId: import.meta.env.VITE_USE_EMULATORS === 'true' ? 'demo-civic-pulse' : (import.meta.env.VITE_FIREBASE_PROJECT_ID || 'civic-pulse-ffac8'),
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || 'civic-pulse-ffac8.firebasestorage.app',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '499580733822',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || '1:499580733822:web:284b540d54b14315148b2f',
  measurementId: 'G-TSWT74SNJV',
}

export const app = initializeApp(firebaseConfig)

export const auth = getAuth(app)
export const db = getFirestore(app)
export const googleProvider = new GoogleAuthProvider()

if (import.meta.env.DEV && import.meta.env.VITE_USE_EMULATORS === 'true') {
  connectAuthEmulator(auth, 'http://127.0.0.1:9099', { disableWarnings: true })
  connectFirestoreEmulator(db, '127.0.0.1', 8080)
}
