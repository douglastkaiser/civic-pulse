import { doc, getDoc, setDoc, deleteDoc, collection, query, where, getDocs, serverTimestamp } from 'firebase/firestore'
import { db } from './firebase'

const COLLECTION = 'organizations'

export async function saveOrg(uid, orgData) {
  const ref = doc(db, COLLECTION, orgData.id)
  await setDoc(ref, {
    ...orgData,
    createdBy: uid,
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp(),
  })
  window.dispatchEvent(new Event('org-created'))
}

export async function loadOrgFromFirestore(orgId) {
  const ref = doc(db, COLLECTION, orgId)
  const snap = await getDoc(ref)
  return snap.exists() ? snap.data() : null
}

export async function loadUserOrgs(uid) {
  const q = query(collection(db, COLLECTION), where('createdBy', '==', uid))
  const snap = await getDocs(q)
  return snap.docs.map((d) => d.data())
}

export async function deleteOrg(orgId) {
  const ref = doc(db, COLLECTION, orgId)
  await deleteDoc(ref)
  window.dispatchEvent(new Event('org-created'))
}
