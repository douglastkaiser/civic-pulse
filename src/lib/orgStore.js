import {
  doc,
  getDoc,
  setDoc,
  collection,
  query,
  where,
  getDocs,
  serverTimestamp,
} from 'firebase/firestore'
import { db, auth } from './firebase'
import { callService } from './service'
export async function saveOrg(uid, orgData) {
  await setDoc(doc(db, 'organizations', orgData.id), {
    ...orgData,
    schema_version: 1,
    createdBy: uid,
    memberIds: [uid],
    members: { [uid]: 'owner' },
    memberLabels: {
      [uid]:
        auth.currentUser?.displayName ||
        auth.currentUser?.email ||
        'Organization owner',
    },
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp(),
  })
}
export async function loadOrgFromFirestore(orgId) {
  const snap = await getDoc(doc(db, 'organizations', orgId))
  return snap.exists() ? snap.data() : null
}
export async function loadPublicOrg(orgId) {
  const snap = await getDoc(doc(db, 'publicOrganizations', orgId))
  if (!snap.exists())
    throw new Error('This organization has not published a public page.')
  return snap.data()
}
export async function loadUserOrgs(uid) {
  const [owned, member] = await Promise.all([
    getDocs(
      query(collection(db, 'organizations'), where('createdBy', '==', uid))
    ),
    getDocs(
      query(
        collection(db, 'organizations'),
        where('memberIds', 'array-contains', uid)
      )
    ),
  ])
  return [
    ...new Map(
      [...owned.docs, ...member.docs].map((d) => [
        d.id,
        { ...d.data(), id: d.id },
      ])
    ).values(),
  ]
}
export function deleteOrg(orgId) {
  return callService('manageOrganization', { operation: 'delete', orgId })
}
