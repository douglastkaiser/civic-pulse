export const AI_RESERVATION_USD = 0.08
export const DAILY_GENERATIONS = 5
export const MONTHLY_BUDGET_USD = 2
export function reserveGeneration(usage, day, month) {
  const daily = usage.day === day ? usage.daily || 0 : 0
  const monthly = usage.month === month ? usage.reservedUSD || 0 : 0
  if (
    daily >= DAILY_GENERATIONS ||
    monthly + AI_RESERVATION_USD > MONTHLY_BUDGET_USD
  )
    throw new Error('Usage limit reached')
  return {
    day,
    month,
    daily: daily + 1,
    reservedUSD: Number((monthly + AI_RESERVATION_USD).toFixed(2)),
  }
}
export function publicOrganization(org) {
  return {
    schema_version: 1,
    name: org.name,
    mission: org.mission,
    tagline: typeof org.tagline === 'string' ? org.tagline : '',
  }
}
export function validInvite(invite, email, now) {
  return (
    !!invite &&
    !invite.acceptedBy &&
    invite.expiresAt > now &&
    invite.email === email.toLowerCase() &&
    ['member', 'organizer'].includes(invite.role)
  )
}
export function notificationCandidates(issues, now) {
  return issues.filter((issue) => {
    const c = issue.public_comment
    return (
      c?.available === true &&
      c.verified === true &&
      typeof c.source_url === 'string' &&
      c.source_url.startsWith('https://') &&
      Number.isFinite(Date.parse(c.verified_at)) &&
      Date.parse(c.verified_at) <= now &&
      now - Date.parse(c.verified_at) <= 7 * 86400000 &&
      /T.*(?:Z|[+-]\d\d:\d\d)$/.test(c.deadline || '') &&
      Date.parse(c.deadline) > now &&
      Date.parse(c.deadline) - now <= 7 * 86400000 &&
      !['canceled', 'passed', 'rejected'].includes(issue.status)
    )
  })
}
