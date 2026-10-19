import registry from '../../shared/jurisdictions.json'
import { fetchJSON as requestJSON } from './request'
import { validateIssueCollection, validateFreshness } from '../../shared/contracts.js'
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

export const ORG_IDS_BY_LOCATION = Object.fromEntries(registry.jurisdictions.map(j => [j.id, j.organizations]))

export const LOCATION_LABELS = Object.fromEntries(registry.jurisdictions.map(j => [j.id, j.label]))

export const ORG_IDS = Object.values(ORG_IDS_BY_LOCATION).flat()

function fetchJSON(path, options) {
  return requestJSON(`${BASE}data/${path}`, options)
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

export function loadIssues(id, options = {}) {
  if (LOCATION_LABELS[id]) {
    return fetchJSON(`issues/${id}.json`, { ...options, validate: validateIssueCollection })
  }
  return loadDynamicIssues(id).then(validateIssueCollection)
}

export function loadFreshness() {
  return fetchJSON('meta/freshness.json', { validate: validateFreshness })
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
  } catch (error) {
    if (error.status !== 404) throw error
    // Static JSON not found — try Firestore for user-created orgs
    const firestoreOrg = await loadOrgFromFirestore(orgId)
    if (firestoreOrg) return normalizeOrgBridgeProvenance(firestoreOrg)
    throw new Error(`Organization not found: ${orgId}`)
  }
}

export async function loadAllOrgs() {
  return Promise.all(ORG_IDS.map((id) => loadOrg(id)))
}
