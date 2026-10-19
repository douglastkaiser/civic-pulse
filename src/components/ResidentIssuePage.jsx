import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { loadIssues } from '../lib/data'
import { useAuth } from '../lib/auth'
import { useActions, saveAction } from '../lib/residentStore'
import {
  issueDeadline,
  sourceAge,
  formatDate,
  JURISDICTIONS,
  verifiedMeeting,
} from '../lib/civic'
import { safeURL } from '../../shared/contracts.js'
import { createCalendarEvent, downloadCalendar } from '../lib/calendar'
import DataState from './shared/DataState'
export default function ResidentIssuePage() {
  const { locationId, issueId } = useParams()
  const { user } = useAuth()
  const { actions, error: actionError } = useActions(user?.uid)
  const [data, setData] = useState(null),
    [error, setError] = useState(null),
    [retry, setRetry] = useState(0),
    [busy, setBusy] = useState(false),
    [draft, setDraft] = useState(''),
    [message, setMessage] = useState('')
  useEffect(() => {
    setData(null)
    setError(null)
    setDraft('')
    setMessage('')
    const controller = new AbortController()
    if (!JURISDICTIONS.some((j) => j.id === locationId)) {
      setError('This location is not covered yet.')
      return
    }
    loadIssues(locationId, { signal: controller.signal })
      .then(setData)
      .catch(() => {
        if (!controller.signal.aborted)
          setError('This issue could not be loaded.')
      })
    return () => controller.abort()
  }, [locationId, issueId, retry])
  const issue = data?.issues.find((i) => i.id === issueId)
  if (!data)
    return (
      <div className="page-wrap">
        <DataState
          loading={!error}
          error={error}
          onRetry={error ? () => setRetry((v) => v + 1) : undefined}
        />
      </div>
    )
  if (!issue)
    return (
      <div className="page-wrap civic-card">
        Issue not found.{' '}
        <Link className="underline" to="/explore">
          Explore other issues
        </Link>
      </div>
    )
  const deadline = issueDeadline(issue),
    source = safeURL(issue.source_url)
  let calendarAvailable = true
  try {
    createCalendarEvent(issue)
  } catch {
    calendarAvailable = false
  }
  const saved = actions.some(
    (a) => a.locationId === locationId && a.issueId === issue.id
  )
  async function save() {
    setBusy(true)
    try {
      await saveAction(user.uid, locationId, issue)
      setMessage('Action saved.')
    } catch {
      setError('This action could not be saved. Please try again.')
    } finally {
      setBusy(false)
    }
  }
  return (
    <div className="page-wrap max-w-4xl space-y-6">
      <Link
        className="text-accent-blue underline"
        to={`/explore?location=${locationId}`}
      >
        ← Back to local issues
      </Link>
      <header>
        <p className="eyebrow">
          {issue.governing_body || 'Local government'} ·{' '}
          {issue.status || 'Status unconfirmed'}
        </p>
        <h1 className="text-3xl md:text-4xl font-semibold mt-3 leading-tight">
          {issue.title}
        </h1>
        <p className="text-sm text-text-secondary mt-4">
          {issue.provenance === 'source_record'
            ? sourceAge({ last_successful_fetch_at: issue.fetched_at })
            : issue.snapshot_at
              ? `Archived snapshot from ${formatDate(issue.snapshot_at)}`
              : 'Snapshot date unknown'}
        </p>
      </header>
      {(error || actionError) && (
        <p role="alert" className="text-accent-red">
          {error || actionError}
        </p>
      )}
      {message && <p role="status">{message}</p>}
      <section className="civic-card">
        <h2 className="text-xl font-semibold mb-3">What is happening</h2>
        {issue.provenance !== 'source_record' && (
          <p className="text-sm text-accent-amber mb-3">
            This is an archived summary. Claims, dates, and instructions need
            current source confirmation.
          </p>
        )}
        {issue.provenance === 'source_record' ? (
          <p className="whitespace-pre-wrap text-text-secondary leading-relaxed">
            {issue.summary}
          </p>
        ) : (
          <>
            <p className="text-text-secondary leading-relaxed">
              {issue.summary.split('\n\n')[0]}
            </p>
            <details className="mt-4">
              <summary className="text-accent-blue cursor-pointer">
                Read the full archived analysis
              </summary>
              <p className="whitespace-pre-wrap text-text-secondary leading-relaxed mt-3">
                {issue.summary}
              </p>
            </details>
          </>
        )}
        {issue.topic_method === 'keyword_navigation_hint' && (
          <p className="text-sm text-text-secondary mt-3">
            Topics are navigation hints assigned from keywords in the official
            record.
          </p>
        )}
      </section>
      <section className="civic-card space-y-3">
        <h2 className="text-xl font-semibold">Dates and participation</h2>
        <p>
          {deadline.actionable
            ? `Verified comment deadline: ${new Date(deadline.at).toLocaleString()}`
            : deadline.expired
              ? 'The recorded comment deadline has passed.'
              : 'A current public comment deadline has not been verified.'}
        </p>
        {verifiedMeeting(issue) ? (
          <p className="text-text-secondary">
            Source-verified meeting:{' '}
            {new Date(issue.meeting.starts_at).toLocaleString([], {
              timeZone: issue.meeting.timezone,
            })}{' '}
            ({issue.meeting.timezone})
          </p>
        ) : (
          issue.meeting_date && (
            <p className="text-text-secondary">
              Recorded meeting date: {formatDate(issue.meeting_date)} · confirm
              with the source
            </p>
          )
        )}
        {deadline.actionable && (
          <p className="text-text-secondary">
            {issue.public_comment.instructions}
          </p>
        )}
        {deadline.source && (
          <a
            className="text-accent-blue underline block"
            href={deadline.source}
            target="_blank"
            rel="noreferrer"
          >
            Check participation instructions ↗
          </a>
        )}
        {source ? (
          <a
            className="text-accent-blue underline block"
            href={source}
            target="_blank"
            rel="noreferrer"
          >
            Read the original source ↗
          </a>
        ) : (
          <p className="text-accent-amber">
            No original source link is available for this record.
          </p>
        )}
        {calendarAvailable && (
          <>
            <button
              className="civic-button"
              onClick={() => downloadCalendar(issue)}
            >
              Add to calendar
            </button>
            <p className="text-sm text-text-secondary">
              Downloaded calendar events do not update automatically. Recheck
              the source for changes.
            </p>
          </>
        )}
      </section>
      <section className="civic-card space-y-4">
        <h2 className="text-xl font-semibold">Choose your next step</h2>
        <p className="text-text-secondary">
          Follow the issue and decide what you want to do. Saved actions and
          notes are private to your account.
        </p>
        {user ? (
          <button
            className="civic-button"
            onClick={save}
            disabled={saved || busy}
          >
            {saved ? 'Saved to your actions' : busy ? 'Saving…' : 'Save action'}
          </button>
        ) : (
          <Link className="civic-button inline-block" to="/signin">
            Sign in to save
          </Link>
        )}
        {source && (
          <div className="pt-4 border-t border-border">
            <h3 className="font-medium">Prepare your own comment</h3>
            <p className="text-sm text-text-secondary mt-2">
              Write in your own words and verify facts at the source. You review
              and submit through the official channel.
            </p>
            <label className="block mt-3">
              Your draft
              <textarea
                className="civic-input mt-2"
                rows={6}
                value={draft}
                onChange={(e) => setDraft(e.target.value)}
                placeholder={`My name is…\nI am commenting on ${issue.title}.\nMy experience is…\nI would like the decision makers to consider…`}
              />
            </label>
            <button
              className="civic-button mt-3"
              disabled={!draft}
              onClick={async () => {
                try {
                  await navigator.clipboard.writeText(draft)
                  setMessage(
                    'Draft copied. Review it before submitting through the official channel.'
                  )
                } catch {
                  setMessage(
                    'Copy is unavailable. Select and copy the draft text.'
                  )
                }
              }}
            >
              Copy reviewed draft
            </button>
            <p className="text-xs text-text-secondary mt-2">
              Draft text stays on this page and is cleared when you leave.
            </p>
          </div>
        )}
      </section>
    </div>
  )
}
