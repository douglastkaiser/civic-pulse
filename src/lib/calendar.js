import { safeURL, validInstant } from '../../shared/contracts.js'
import { issueDeadline, verifiedMeeting } from './civic.js'
function escapeText(value) {
  return String(value || '')
    .replaceAll('\\', '\\\\')
    .replaceAll('\n', '\\n')
    .replaceAll(',', '\\,')
    .replaceAll(';', '\\;')
    .replaceAll('\r', '')
}
function timestamp(value) {
  return new Date(value)
    .toISOString()
    .replace(/[-:]/g, '')
    .replace(/\.\d{3}/, '')
}
export function createCalendarEvent(issue, now = Date.now()) {
  const deadline = issueDeadline(issue, now)
  const meeting = issue.meeting
  const validMeeting = verifiedMeeting(issue, now)
  if (
    ['canceled', 'passed', 'rejected'].includes(issue.status) ||
    (!deadline.actionable && !validMeeting)
  )
    throw new Error('A verified upcoming date is required for calendar export.')
  const start = deadline.actionable ? deadline.at : meeting.starts_at
  const end = deadline.actionable
    ? new Date(Date.parse(start) + 15 * 60000).toISOString()
    : validInstant(meeting.ends_at) &&
        Date.parse(meeting.ends_at) > Date.parse(start)
      ? meeting.ends_at
      : new Date(Date.parse(start) + 3600000).toISOString()
  const source = deadline.actionable
    ? deadline.source
    : safeURL(meeting.source_url)
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Civic Pulse//EN',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    'BEGIN:VEVENT',
    `UID:${escapeText(issue.id)}-${deadline.actionable ? 'comment' : 'meeting'}@civic-pulse`,
    `DTSTAMP:${timestamp(now)}`,
    `DTSTART:${timestamp(start)}`,
    `DTEND:${timestamp(end)}`,
    `SUMMARY:${escapeText(deadline.actionable ? `Comment deadline: ${issue.title}` : issue.title)}`,
    `DESCRIPTION:${escapeText(`Verify changes or cancellations at ${source}. Calendar downloads do not update automatically. Original time zone: ${meeting?.timezone || issue.timezone || 'See source'}.`)}`,
    `URL:${source}`,
    'END:VEVENT',
    'END:VCALENDAR',
  ]
  // Fold at UTF-8 octet boundaries (RFC 5545), without splitting a Unicode character.
  return (
    lines
      .flatMap((line) => {
        const result = []
        let part = ''
        let bytes = 0
        for (const char of line) {
          const size = new TextEncoder().encode(char).length
          if (bytes + size > 74) {
            result.push(part)
            part = ' '
            bytes = 1
          }
          part += char
          bytes += size
        }
        result.push(part)
        return result
      })
      .join('\r\n') + '\r\n'
  )
}
export function downloadCalendar(issue) {
  const data = createCalendarEvent(issue)
  const url = URL.createObjectURL(
    new Blob([data], { type: 'text/calendar;charset=utf-8' })
  )
  const a = document.createElement('a')
  a.href = url
  a.download = 'civic-pulse-event.ics'
  a.click()
  URL.revokeObjectURL(url)
}
