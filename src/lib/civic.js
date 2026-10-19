import registry from '../../shared/jurisdictions.json' with { type: 'json' }
import { safeURL, validInstant } from '../../shared/contracts.js'
export const JURISDICTIONS = registry.jurisdictions
export function coverageLabel(id) {
  const jurisdiction = JURISDICTIONS.find((j) => j.id === id)
  return jurisdiction?.coverage === 'partial'
    ? 'Partial coverage'
    : jurisdiction?.coverage === 'snapshot'
      ? 'Archived snapshot · automatic updates unavailable'
      : 'Coverage unavailable'
}
export function issueDeadline(issue, now = Date.now()) {
  const deadline = issue.public_comment?.deadline
  const source = safeURL(issue.public_comment?.source_url)
  const verified =
    issue.public_comment?.verified === true &&
    validInstant(issue.public_comment?.verified_at) &&
    Date.parse(issue.public_comment.verified_at) <= now &&
    now - Date.parse(issue.public_comment.verified_at) <= 7 * 86400000 &&
    validInstant(deadline) &&
    !!source
  const expired = validInstant(deadline) && Date.parse(deadline) <= now
  const closed = ['passed', 'rejected', 'canceled'].includes(issue.status)
  return {
    at: validInstant(deadline) ? deadline : null,
    source,
    verified,
    expired,
    actionable:
      verified &&
      !expired &&
      !closed &&
      issue.public_comment.available === true,
  }
}
export function isCurrentIssue(issue, now = Date.now()) {
  return (
    !['passed', 'rejected', 'canceled'].includes(issue.status) &&
    (!issue.meeting_date ||
      Date.parse(issue.meeting_date.slice(0, 10) + 'T23:59:59Z') >= now)
  )
}
export function relevance(issue, preferences) {
  const matching = issue.policy_domains.filter((d) =>
    preferences?.interests?.some((i) => {
      const aliases = {
        Budget: ['budget', 'taxation', 'finance'],
        Environment: ['environment', 'climate'],
        Education: ['education', 'school'],
        Healthcare: ['health'],
      }
      return (aliases[i] || [i.toLowerCase()]).some((term) =>
        d.toLowerCase().includes(term)
      )
    })
  )
  return {
    score: matching.length,
    reason: matching.length
      ? `Matches your interests: ${matching.join(', ')}`
      : 'Local decision in your selected area',
  }
}
export function formatDate(value) {
  if (!value || !Number.isFinite(Date.parse(value))) return 'Date unconfirmed'
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    ...(/^\d{4}-\d\d-\d\d$/.test(value) ? { timeZone: 'UTC' } : {}),
  }).format(new Date(value))
}
export function sourceAge(data) {
  const value = data?.last_successful_fetch_at || data?.last_scraped
  if (!value || !Number.isFinite(Date.parse(value)))
    return 'Last checked: unknown'
  return `Last checked ${formatDate(value)}${Date.now() - Date.parse(value) > 7 * 86400000 ? ' · information may be out of date' : ''}`
}
export function verifiedMeeting(issue, now = Date.now()) {
  const meeting = issue.meeting
  return (
    !!meeting &&
    meeting.verified === true &&
    validInstant(meeting.verified_at) &&
    Date.parse(meeting.verified_at) <= now &&
    now - Date.parse(meeting.verified_at) <= 7 * 86400000 &&
    validInstant(meeting.starts_at) &&
    Date.parse(meeting.starts_at) > now &&
    !!safeURL(meeting.source_url) &&
    typeof meeting.timezone === 'string' &&
    !['canceled', 'passed', 'rejected'].includes(issue.status)
  )
}
export function opportunityTime(issue, now = Date.now()) {
  return issueDeadline(issue, now).actionable
    ? issueDeadline(issue, now).at
    : verifiedMeeting(issue, now)
      ? issue.meeting.starts_at
      : null
}
