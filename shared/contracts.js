/** Shared runtime contracts for data entering the UI and API. */
export const SCHEMA_VERSION = 1
export const ACTION_STATES = ['saved', 'planned', 'completed', 'dismissed']
export const ISSUE_STATES = [
  'upcoming',
  'passed',
  'rejected',
  'postponed',
  'amended',
  'canceled',
  'unresolved',
]
export function safeURL(value) {
  try {
    const url = new URL(value)
    return ['https:', 'http:'].includes(url.protocol) ? url.href : null
  } catch {
    return null
  }
}
export function validInstant(value) {
  return (
    typeof value === 'string' &&
    /T.*(?:Z|[+-]\d\d:\d\d)$/.test(value) &&
    Number.isFinite(Date.parse(value))
  )
}
export function validateIssue(issue) {
  if (
    !issue ||
    typeof issue.id !== 'string' ||
    !issue.id ||
    typeof issue.title !== 'string' ||
    !issue.title
  )
    throw new Error('Issue needs an ID and title.')
  if (
    typeof issue.summary !== 'string' ||
    !Array.isArray(issue.policy_domains) ||
    issue.policy_domains.some((d) => typeof d !== 'string')
  )
    throw new Error('Invalid issue summary or topics.')
  if (issue.source_url != null && !safeURL(issue.source_url))
    throw new Error('Invalid issue source URL.')
  if (issue.schema_version != null && issue.schema_version !== SCHEMA_VERSION)
    throw new Error('Unsupported issue version.')
  return issue
}
export function validateIssueCollection(data) {
  if (!data || !Array.isArray(data.issues))
    throw new Error('Issue coverage is temporarily unavailable.')
  if (data.schema_version != null && data.schema_version !== SCHEMA_VERSION)
    throw new Error('Unsupported issue data version.')
  const ids = new Set()
  data.issues.forEach((issue) => {
    validateIssue(issue)
    if (ids.has(issue.id)) throw new Error('Duplicate issue ID.')
    ids.add(issue.id)
  })
  return data
}
export function validatePreferences(data, jurisdictionIds) {
  if (!jurisdictionIds.includes(data.locationId))
    throw new Error('Choose a listed location.')
  if (
    !Array.isArray(data.interests) ||
    data.interests.some((i) => typeof i !== 'string' || i.length > 100) ||
    data.interests.length > 20
  )
    throw new Error('Choose up to 20 interests.')
  if (![5, 15, 30, 60].includes(data.availableMinutes))
    throw new Error('Choose an available time.')
  return data
}
export function validateAction(data) {
  if (
    !ACTION_STATES.includes(data.state) ||
    typeof data.issueId !== 'string' ||
    typeof data.locationId !== 'string'
  )
    throw new Error('Invalid saved action.')
  if (typeof data.notes !== 'string' || data.notes.length > 4000)
    throw new Error('Notes must be under 4,000 characters.')
  return data
}
export function validateGeneratedProfile(data) {
  if (
    !data?.manifesto ||
    typeof data.manifesto.manifesto_summary !== 'string' ||
    typeof data.manifesto.narrative !== 'string'
  )
    throw new Error('Invalid generated profile.')
  const compass = data.political_compass?.user
  if (
    !compass ||
    !['economic', 'social'].every(
      (k) => Number.isFinite(compass[k]) && Math.abs(compass[k]) <= 1
    )
  )
    throw new Error('Invalid profile coordinates.')
  if (
    !Array.isArray(data.political_positions) ||
    !data.political_positions.length ||
    data.political_positions.length > 50
  )
    throw new Error('Invalid profile positions.')
  for (const p of data.political_positions) {
    if (
      typeof p.id !== 'string' ||
      typeof p.question !== 'string' ||
      !Number.isFinite(p.position) ||
      Math.abs(p.position) > 1 ||
      !Number.isInteger(p.importance) ||
      p.importance < 1 ||
      p.importance > 5
    )
      throw new Error('Invalid profile position.')
  }
  for (const k of ['values', 'issue_salience', 'political_context'])
    if (!data[k] || typeof data[k] !== 'object' || Array.isArray(data[k]))
      throw new Error(`Invalid ${k}.`)
  return data
}

export function validateFreshness(data) {
  if (
    !data ||
    typeof data.locations !== 'object' ||
    Array.isArray(data.locations)
  )
    throw new Error('Invalid source health data.')
  if (data.schema_version != null && data.schema_version !== SCHEMA_VERSION)
    throw new Error('Unsupported source health version.')
  for (const record of Object.values(data.locations)) {
    if (
      record.needs_rescrape != null &&
      typeof record.needs_rescrape !== 'boolean'
    )
      throw new Error('Invalid source health flag.')
    if (
      record.status != null &&
      !['updated', 'no_changes', 'failed', 'unsupported'].includes(
        record.status
      )
    )
      throw new Error('Invalid source health status.')
    for (const field of [
      'last_attempt_at',
      'last_successful_fetch_at',
      'last_successful_generation_at',
    ])
      if (record[field] != null && !validInstant(record[field]))
        throw new Error('Invalid source health timestamp.')
  }
  return data
}
