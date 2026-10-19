import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync, readdirSync } from 'node:fs'
import {
  validateIssueCollection,
  validatePreferences,
  validateAction,
  safeURL,
  validateGeneratedProfile,
  validateFreshness,
} from '../shared/contracts.js'
import {
  reserveGeneration,
  publicOrganization,
  validInvite,
  notificationCandidates,
} from '../functions/policy.js'
const fixture = {
  id: 'one',
  title: 'Meeting',
  summary: 'A decision',
  policy_domains: [],
  source_url: 'https://example.gov',
}
test('published issue files satisfy the boundary contract', () => {
  for (const file of readdirSync('public/data/issues').filter(
    (f) => f.endsWith('.json') && !f.endsWith('-raw.json')
  ))
    validateIssueCollection(
      JSON.parse(readFileSync(`public/data/issues/${file}`))
    )
})
test('malformed or duplicate data is rejected before publishing', () => {
  assert.throws(() => validateIssueCollection({ issues: [fixture, fixture] }))
  assert.throws(() =>
    validateIssueCollection({ issues: [{ ...fixture, policy_domains: null }] })
  )
  assert.throws(() =>
    validateIssueCollection({ schema_version: 99, issues: [] })
  )
  assert.equal(safeURL('javascript:alert(1)'), null)
})
test('onboarding and actions enforce choices and note bounds', () => {
  assert.throws(() =>
    validatePreferences(
      { locationId: 'unknown', interests: [], availableMinutes: 5 },
      ['austin-78702']
    )
  )
  assert.throws(() =>
    validateAction({
      issueId: 'one',
      locationId: 'austin',
      state: 'other',
      notes: '',
    })
  )
  assert.throws(() =>
    validateAction({
      issueId: 'one',
      locationId: 'austin',
      state: 'saved',
      notes: 'x'.repeat(4001),
    })
  )
})
test('generation reservations enforce daily and monthly spending limits', () => {
  assert.equal(reserveGeneration({}, '2026-10-18', '2026-10').reservedUSD, 0.08)
  assert.throws(() =>
    reserveGeneration(
      { day: '2026-10-18', month: '2026-10', daily: 5, reservedUSD: 0.4 },
      '2026-10-18',
      '2026-10'
    )
  )
  assert.throws(() =>
    reserveGeneration(
      { month: '2026-10', reservedUSD: 2 },
      '2026-10-19',
      '2026-10'
    )
  )
  assert.equal(
    reserveGeneration(
      { day: 'old', month: 'old', daily: 100, reservedUSD: 100 },
      'new',
      'new'
    ).daily,
    1
  )
})
test('public organization projection cannot expose members or tasks', () => {
  assert.deepEqual(
    Object.keys(
      publicOrganization({
        name: 'Group',
        mission: 'Purpose',
        memberIds: ['private'],
        tasks: ['private'],
        email: 'private',
      })
    ).sort(),
    ['mission', 'name', 'schema_version', 'tagline']
  )
})
test('invites require the intended verified identity and cannot be reused', () => {
  const invite = {
    email: 'resident@example.com',
    role: 'member',
    expiresAt: 1000,
  }
  assert.equal(validInvite(invite, 'resident@example.com', 100), true)
  assert.equal(validInvite(invite, 'other@example.com', 100), false)
  assert.equal(validInvite(invite, invite.email, 1001), false)
  assert.equal(
    validInvite({ ...invite, acceptedBy: 'someone' }, invite.email, 100),
    false
  )
})
test('notifications exclude expired, canceled, and unverified opportunities', () => {
  const now = Date.parse('2026-10-18T12:00:00Z')
  const issue = {
    ...fixture,
    public_comment: {
      available: true,
      verified: true,
      verified_at: '2026-10-18T10:00:00Z',
      source_url: 'https://example.gov',
      deadline: '2026-10-19T12:00:00Z',
    },
  }
  assert.equal(notificationCandidates([issue], now).length, 1)
  for (const invalid of [
    { ...issue, status: 'canceled' },
    {
      ...issue,
      public_comment: {
        ...issue.public_comment,
        deadline: '2026-01-01T00:00:00Z',
      },
    },
    { ...issue, public_comment: { ...issue.public_comment, verified: false } },
  ])
    assert.equal(notificationCandidates([invalid], now).length, 0)
})

test('malformed AI profiles cannot replace valid resident data', () => {
  assert.throws(() =>
    validateGeneratedProfile({
      manifesto: { manifesto_summary: 'Summary', narrative: 'Narrative' },
      political_compass: { user: { economic: 99, social: 0 } },
    })
  )
  assert.throws(() =>
    validateGeneratedProfile({
      manifesto: { manifesto_summary: {}, narrative: 'Narrative' },
    })
  )
})

test('source health flags stay boolean and attempts cannot masquerade as successful fetches', () => {
  validateFreshness(JSON.parse(readFileSync('public/data/meta/freshness.json')))
  assert.throws(() =>
    validateFreshness({
      locations: { austin: { needs_rescrape: '2026-10-18T12:00:00Z' } },
    })
  )
  assert.throws(() =>
    validateFreshness({
      locations: { austin: { last_successful_fetch_at: 'unknown' } },
    })
  )
})
