import { useEffect, useState } from 'react'
import {
  doc,
  collection,
  onSnapshot,
  setDoc,
  updateDoc,
  serverTimestamp,
  getDocs,
  writeBatch,
  deleteDoc,
  runTransaction,
} from 'firebase/firestore'
import { db } from './firebase'
import { validateAction, validatePreferences } from '../../shared/contracts.js'
import { JURISDICTIONS } from './civic'

export function useResident(uid) {
  const [state, setState] = useState({
    profile: null,
    loading: true,
    error: null,
  })
  useEffect(() => {
    setState({ uid, profile: null, loading: !!uid, error: null })
    if (!uid) return
    return onSnapshot(
      doc(db, 'users', uid),
      (snapshot) =>
        setState({
          uid,
          profile: snapshot.exists() ? snapshot.data() : null,
          loading: false,
          error: null,
        }),
      () =>
        setState({
          uid,
          profile: null,
          loading: false,
          error:
            'Your profile could not be loaded. Check your connection and retry.',
        })
    )
  }, [uid])
  return state.uid === uid
    ? state
    : { profile: null, loading: !!uid, error: null }
}
export function savePreferences(uid, preferences) {
  validatePreferences(
    preferences,
    JURISDICTIONS.map((j) => j.id)
  )
  return setDoc(
    doc(db, 'users', uid),
    {
      preferences,
      locations: [{ id: preferences.locationId, primary: true }],
      schema_version: 1,
      updatedAt: serverTimestamp(),
    },
    { merge: true }
  )
}
export function actionId(locationId, issueId) {
  return encodeURIComponent(`${locationId}:${issueId}`)
}
export function useActions(uid) {
  const [state, setState] = useState({
    actions: [],
    loading: !!uid,
    error: null,
  })
  useEffect(() => {
    setState({ uid, actions: [], loading: !!uid, error: null })
    if (!uid) return
    return onSnapshot(
      collection(db, 'users', uid, 'actions'),
      (snapshot) =>
        setState({
          uid,
          actions: snapshot.docs.map((d) => ({ ...d.data(), id: d.id })),
          loading: false,
          error: null,
        }),
      () =>
        setState({
          uid,
          actions: [],
          loading: false,
          error: 'Saved actions could not be loaded. Please retry.',
        })
    )
  }, [uid])
  return state.uid === uid
    ? state
    : { actions: [], loading: !!uid, error: null }
}
export function saveAction(uid, locationId, issue) {
  const data = validateAction({
    schema_version: 1,
    issueId: issue.id,
    locationId,
    title: issue.title,
    state: 'saved',
    notes: '',
  })
  const ref = doc(db, 'users', uid, 'actions', actionId(locationId, issue.id))
  return runTransaction(db, async (transaction) => {
    const existing = await transaction.get(ref)
    if (!existing.exists())
      transaction.set(ref, {
        ...data,
        createdAt: serverTimestamp(),
        updatedAt: serverTimestamp(),
      })
  })
}
export function updateAction(uid, id, changes) {
  if (
    changes.state &&
    !['saved', 'planned', 'completed', 'dismissed'].includes(changes.state)
  )
    throw new Error('Invalid state')
  if (
    changes.notes != null &&
    (typeof changes.notes !== 'string' || changes.notes.length > 4000)
  )
    throw new Error('Notes must be under 4,000 characters.')
  return updateDoc(doc(db, 'users', uid, 'actions', id), {
    ...changes,
    updatedAt: serverTimestamp(),
  })
}
export function removeAction(uid, id) {
  return deleteDoc(doc(db, 'users', uid, 'actions', id))
}
export async function exportResident(uid) {
  const { getUserProfile } = await import('./userStore')
  const [profile, actions] = await Promise.all([
    getUserProfile(uid),
    getDocs(collection(db, 'users', uid, 'actions')),
  ])
  return {
    schema_version: 1,
    exported_at: new Date().toISOString(),
    profile,
    actions: actions.docs.map((d) => d.data()),
  }
}
export function downloadJSON(data, filename) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  )
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}
// Used for local emulator cleanup only; production deletion also removes server-owned records.
export async function deleteActionBatch(uid) {
  const snapshot = await getDocs(collection(db, 'users', uid, 'actions'))
  for (let offset = 0; offset < snapshot.docs.length; offset += 400) {
    const batch = writeBatch(db)
    snapshot.docs
      .slice(offset, offset + 400)
      .forEach((d) => batch.delete(d.ref))
    await batch.commit()
  }
}
