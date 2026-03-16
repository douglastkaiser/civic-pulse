const BASE = import.meta.env.BASE_URL

export const PROFILE_IDS = [
  'austin-78702',
  'brooklyn-ny',
  'madison-wi',
  'cambridge-ma',
  'brookline-ma',
]

async function fetchJSON(path) {
  const res = await fetch(`${BASE}data/${path}`)
  if (!res.ok) throw new Error(`Failed to fetch ${path}: ${res.status}`)
  return res.json()
}

export function loadProfile(id) {
  return fetchJSON(`profiles/${id}.json`)
}

export function loadLocation(id) {
  return fetchJSON(`locations/${id}.json`)
}

export function loadIssues(id) {
  return fetchJSON(`issues/${id}.json`)
}

export function loadFreshness() {
  return fetchJSON('meta/freshness.json')
}

export async function loadAllProfiles() {
  return Promise.all(PROFILE_IDS.map((id) => loadProfile(id)))
}
