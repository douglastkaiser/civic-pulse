import { loadDynamicLocation, loadDynamicIssues } from './locationStore'
import { loadOrgFromFirestore } from './orgStore'
import { normalizeLocationBridgeProvenance, normalizeOrgBridgeProvenance } from './bridgeProvenance'

const BASE = import.meta.env.BASE_URL

export const PROFILE_IDS = [
  'austin-78702',
  'brooklyn-ny',
  'madison-wi',
  'cambridge-ma',
  'brookline-ma',
]

export const PROFILE_ID = 'doug'

export const ORG_IDS_BY_LOCATION = {
  'austin-78702': ['austin-yimby-action', 'austin-abundance-project', 'austin-safe-and-sound'],
  'orange-92868': ['oc-housing-now', 'oc-purple-accountability', 'oc-abundance-project'],
}

export const LOCATION_LABELS = {
  'austin-78702': 'Austin, TX',
  'orange-92868': 'Orange County, CA',
}

export const ORG_IDS = Object.values(ORG_IDS_BY_LOCATION).flat()

async function fetchJSON(path) {
  const res = await fetch(`${BASE}data/${path}`)
  if (!res.ok) throw new Error(`Failed to fetch ${path}: ${res.status}`)
  return res.json()
}

export function loadProfile(id) {
  return fetchJSON(`profiles/${id}.json`)
}

export function loadLocation(id) {
  if (LOCATION_LABELS[id]) {
    return fetchJSON(`locations/${id}.json`).then(normalizeLocationBridgeProvenance)
  }
  return loadDynamicLocation(id).then(normalizeLocationBridgeProvenance)
}

export function loadIssues(id) {
  if (LOCATION_LABELS[id]) {
    return fetchJSON(`issues/${id}.json`)
  }
  return loadDynamicIssues(id)
}

export function loadFreshness() {
  return fetchJSON('meta/freshness.json')
}

export async function loadAllProfiles() {
  return Promise.all(PROFILE_IDS.map((id) => loadProfile(id)))
}

export function loadOfficials(locationId) {
  return fetchJSON(`officials/${locationId}.json`)
}

export async function loadOrg(orgId) {
  try {
    const org = await fetchJSON(`orgs/${orgId}.json`)
    return normalizeOrgBridgeProvenance(org)
  } catch {
    // Static JSON not found — try Firestore for user-created orgs
    const firestoreOrg = await loadOrgFromFirestore(orgId)
    if (firestoreOrg) return normalizeOrgBridgeProvenance(firestoreOrg)
    throw new Error(`Organization not found: ${orgId}`)
  }
}

export async function loadAllOrgs() {
  return Promise.all(ORG_IDS.map((id) => loadOrg(id)))
}
