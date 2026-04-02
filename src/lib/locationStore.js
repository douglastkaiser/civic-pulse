import { doc, getDoc, setDoc, serverTimestamp } from 'firebase/firestore'
import { db } from './firebase'

export async function saveLocation(locationId, data) {
  await setDoc(doc(db, 'locations', locationId), {
    ...data,
    updatedAt: serverTimestamp(),
  })
}

export async function loadDynamicLocation(locationId) {
  const snap = await getDoc(doc(db, 'locations', locationId))
  if (!snap.exists()) throw new Error(`Location ${locationId} not found`)
  return snap.data()
}

export async function saveLocationIssues(locationId, data) {
  await setDoc(doc(db, 'locationIssues', locationId), {
    ...data,
    updatedAt: serverTimestamp(),
  })
}

export async function loadDynamicIssues(locationId) {
  const snap = await getDoc(doc(db, 'locationIssues', locationId))
  if (!snap.exists()) throw new Error(`Issues for ${locationId} not found`)
  return snap.data()
}

export async function getDynamicLocationLabels() {
  const snap = await getDoc(doc(db, 'locationRegistry', 'all'))
  if (!snap.exists()) return {}
  return snap.data().locations || {}
}

export async function registerLocation(locationId, label) {
  await setDoc(
    doc(db, 'locationRegistry', 'all'),
    { locations: { [locationId]: label }, updatedAt: serverTimestamp() },
    { merge: true }
  )
}
