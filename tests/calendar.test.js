import { test } from 'node:test'
import assert from 'node:assert/strict'
import { createCalendarEvent } from '../src/lib/calendar.js'
import { issueDeadline } from '../src/lib/civic.js'
const now = Date.parse('2026-10-18T12:00:00Z')
const issue = {
  id: 'hearing',
  title: 'Housing; a decision, together',
  timezone: 'America/Chicago',
  public_comment: {
    available: true,
    verified: true,
    verified_at: '2026-10-18T10:00:00Z',
    source_url: 'https://example.gov/comments',
    deadline: '2026-10-20T18:00:00-05:00',
  },
}
test('calendar preserves an exact source-verified instant and stable event UID', () => {
  const calendar = createCalendarEvent(issue, now)
  assert.match(calendar, /DTSTART:20261020T230000Z/)
  assert.match(calendar, /UID:hearing-comment@civic-pulse/)
  assert.ok(calendar.includes('Housing\\; a decision\\, together'))
  assert.ok(calendar.endsWith('\r\n'))
})
test('unverified, stale, canceled and expired dates cannot produce calendar prompts', () => {
  for (const invalid of [
    { ...issue, status: 'canceled' },
    { ...issue, public_comment: { ...issue.public_comment, verified: false } },
    {
      ...issue,
      public_comment: {
        ...issue.public_comment,
        verified_at: '2026-01-01T00:00:00Z',
      },
    },
    {
      ...issue,
      public_comment: {
        ...issue.public_comment,
        deadline: '2026-10-01T10:00:00Z',
      },
    },
    {
      ...issue,
      public_comment: {
        ...issue.public_comment,
        deadline: 'October 20, sometime',
      },
    },
  ]) {
    assert.throws(() => createCalendarEvent(invalid, now))
    assert.equal(issueDeadline(invalid, now).actionable, false)
  }
})
test('verified meeting dates work without inventing public comment availability', () => {
  const meeting = {
    id: 'meeting',
    title: 'Council hearing',
    meeting: {
      verified: true,
      verified_at: '2026-10-18T10:00:00Z',
      starts_at: '2026-10-19T10:00:00-05:00',
      timezone: 'America/Chicago',
      source_url: 'https://example.gov/agenda',
    },
  }
  assert.match(createCalendarEvent(meeting, now), /DTSTART:20261019T150000Z/)
})
