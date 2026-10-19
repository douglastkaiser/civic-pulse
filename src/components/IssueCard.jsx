import { Link } from 'react-router-dom'
import { safeURL } from '../../shared/contracts.js'
import {
  issueDeadline,
  formatDate,
  relevance,
  verifiedMeeting,
} from '../lib/civic'
export default function IssueCard({
  issue,
  locationId,
  preferences,
  saved,
  onSave,
  busy,
}) {
  const deadline = issueDeadline(issue)
  const source = safeURL(issue.source_url)
  return (
    <article className="issue-row flex flex-col gap-2">
      <div className="flex flex-wrap gap-2 text-xs text-text-secondary">
        <span>{issue.governing_body || 'Local government'}</span>
        <span>· {issue.status || 'Status unconfirmed'}</span>
        {issue.provenance !== 'source_record' && (
          <span className="text-accent-amber">
            Unverified archive
            {issue.snapshot_at
              ? ` · ${formatDate(issue.snapshot_at)}`
              : ' · date unknown'}
          </span>
        )}
      </div>
      <h2 className="text-base font-semibold leading-snug">
        <Link
          to={`/issues/${locationId}/${encodeURIComponent(issue.id)}`}
          className="hover:underline"
        >
          {issue.title}
        </Link>
      </h2>
      <p className="text-sm text-text-secondary leading-relaxed line-clamp-2">
        {issue.summary}
      </p>
      <div className="flex flex-wrap gap-2">
        {issue.policy_domains.map((topic) => (
          <span
            key={topic}
            className="issue-topic"
          >
            {topic}
          </span>
        ))}
      </div>
      {preferences && (
        <p className="text-sm text-accent-green">
          {relevance(issue, preferences).reason}
        </p>
      )}
      <p className="text-sm text-text-secondary">
        {deadline.actionable
          ? `Comment by ${formatDate(deadline.at)}`
          : verifiedMeeting(issue)
            ? `Meeting ${formatDate(issue.meeting.starts_at)} · ${new Date(issue.meeting.starts_at).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', timeZone: issue.meeting.timezone })} (${issue.meeting.timezone})`
            : deadline.expired
              ? 'Comment deadline has passed'
              : 'Participation dates need confirmation'}
        {issue.fetched_at && ` · Checked ${formatDate(issue.fetched_at)}`}
      </p>
      <div className="mt-auto flex flex-wrap items-center gap-3">
        <Link
          className="text-accent-blue underline"
          to={`/issues/${locationId}/${encodeURIComponent(issue.id)}`}
        >
          Understand this issue
        </Link>
        {source && (
          <a
            className="text-sm text-text-secondary underline"
            href={source}
            target="_blank"
            rel="noreferrer"
          >
            Original source ↗
          </a>
        )}
        {onSave ? (
          <button
            className="civic-button ml-auto"
            disabled={busy || saved}
            onClick={onSave}
          >
            {saved ? 'Saved' : busy ? 'Saving…' : 'Save action'}
          </button>
        ) : (
          <Link className="civic-button ml-auto" to="/signin">
            Sign in to save
          </Link>
        )}
      </div>
    </article>
  )
}
