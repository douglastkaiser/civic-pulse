import { doc, getDoc, setDoc, serverTimestamp } from 'firebase/firestore'
import { db } from './firebase'

function userDoc(uid) {
  return doc(db, 'users', uid)
}

export async function getUserProfile(uid) {
  const snap = await getDoc(userDoc(uid))
  return snap.exists() ? snap.data() : null
}

export async function saveUserProfile(uid, data) {
  await setDoc(userDoc(uid), { ...data, updatedAt: serverTimestamp() }, { merge: true })
}

export function emptyProfile(user) {
  return {
    display_name: user.displayName || '',
    email: user.email || '',
    photoURL: user.photoURL || '',
    locations: [],
    values: [],
    issue_salience: {},
    manifesto: null,
    political_compass: null,
    engagement_appetite: null,
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp(),
  }
}

export async function initUserProfile(user) {
  const existing = await getUserProfile(user.uid)
  if (existing) return existing
  const profile = emptyProfile(user)
  await setDoc(userDoc(user.uid), profile)
  return profile
}
