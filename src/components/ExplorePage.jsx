import { useEffect, useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { loadIssues } from '../lib/data'
import {
  JURISDICTIONS,
  coverageLabel,
  sourceAge,
  isCurrentIssue,
  issueDeadline,
  opportunityTime,
} from '../lib/civic'
import { useAuth } from '../lib/auth'
import { saveAction, useActions } from '../lib/residentStore'
import IssueCard from './IssueCard'
import DataState from './shared/DataState'
export default function ExplorePage() {
  const [params, setParams] = useSearchParams()
  const locationId = JURISDICTIONS.some((j) => j.id === params.get('location'))
    ? params.get('location')
    : JURISDICTIONS[0].id
  const [data, setData] = useState(null),
    [error, setError] = useState(null),
    [retry, setRetry] = useState(0),
    [busy, setBusy] = useState(null)
  const [limit, setLimit] = useState(20)
  const [query, setQuery] = useState(''),
    [topic, setTopic] = useState(''),
    [timing, setTiming] = useState('all'),
    [sort, setSort] = useState('recent')
  const { user } = useAuth()
  const { actions, error: actionError } = useActions(user?.uid)
  useEffect(() => {
    setData(null)
    setError(null)
    setTopic('')
    const controller = new AbortController()
    loadIssues(locationId, { signal: controller.signal })
      .then(setData)
      .catch(() => {
        if (!controller.signal.aborted)
          setError(
            'Coverage is temporarily unavailable. Your saved actions are safe.'
          )
      })
    return () => controller.abort()
  }, [locationId, retry])
  const topics = useMemo(
    () =>
      [...new Set(data?.issues.flatMap((i) => i.policy_domains) || [])].sort(),
    [data]
  )
  const filtered = useMemo(
    () =>
      (data?.issues || [])
        .filter(
          (i) =>
            `${i.title} ${i.summary} ${i.governing_body}`
              .toLowerCase()
              .includes(query.toLowerCase()) &&
            (!topic || i.policy_domains.includes(topic)) &&
            (timing === 'all' ||
              (timing === 'current' ? isCurrentIssue(i) : !!opportunityTime(i)))
        )
        .sort((a, b) =>
          sort === 'title'
            ? a.title.localeCompare(b.title)
            : (Date.parse(b.fetched_at || b.snapshot_at) || 0) -
              (Date.parse(a.fetched_at || a.snapshot_at) || 0)
        ),
    [data, query, topic, timing, sort]
  )
  useEffect(() => {
    setLimit(20)
  }, [locationId, query, topic, timing, sort])
  async function save(issue) {
    setBusy(issue.id)
    try {
      await saveAction(user.uid, locationId, issue)
    } catch {
      setError('Could not save this action. Please try again.')
    } finally {
      setBusy(null)
    }
  }
  return (
    <div className="page-wrap space-y-6">
      <header>
        <p className="eyebrow">Understand what is happening near you</p>
        <h1 className="text-4xl font-semibold mt-3">Explore your community</h1>
        <div className="flex flex-wrap gap-4 mt-4 text-sm text-accent-blue underline">
          <Link to={`/officials/${locationId}`}>Who represents you</Link>
          <Link to={`/elections/${locationId}`}>Election reference</Link>
          <Link to="/location/new">Request another area</Link>
        </div>
      </header>
      <div className="civic-card grid sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <label>
          Area
          <select
            className="civic-input mt-2"
            value={locationId}
            onChange={(e) => setParams({ location: e.target.value })}
          >
            {JURISDICTIONS.map((j) => (
              <option key={j.id} value={j.id}>
                {j.label}
              </option>
            ))}
          </select>
        </label>
        <label>
          Search
          <input
            className="civic-input mt-2"
            type="search"
            placeholder="Find an issue…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
        <label>
          Topic
          <select
            className="civic-input mt-2"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          >
            <option value="">All topics</option>
            {topics.map((t) => (
              <option key={t}>{t}</option>
            ))}
          </select>
        </label>
        <label>
          Timing
          <select
            className="civic-input mt-2"
            value={timing}
            onChange={(e) => setTiming(e.target.value)}
          >
            <option value="all">All records</option>
            <option value="current">Current or undated</option>
            <option value="deadline">Verified dates</option>
          </select>
        </label>
        <label>
          Sort
          <select
            className="civic-input mt-2"
            value={sort}
            onChange={(e) => setSort(e.target.value)}
          >
            <option value="title">Title</option>
            <option value="recent">Recently checked</option>
          </select>
        </label>
      </div>
      <p className="text-sm text-text-secondary">
        {coverageLabel(locationId)} · {sourceAge(data)}
      </p>
      {(error || actionError) && (
        <DataState
          error={error || actionError}
          onRetry={() => setRetry((v) => v + 1)}
        />
      )}
      {!data && !error && <DataState loading />}
      {data && (
        <>
          <p role="status" className="text-text-secondary">
            {filtered.length} matching issues
          </p>
          <div className="issue-list">
            {filtered.slice(0, limit).map((issue) => (
              <IssueCard
                key={issue.id}
                issue={issue}
                locationId={locationId}
                saved={actions.some(
                  (a) => a.issueId === issue.id && a.locationId === locationId
                )}
                onSave={user ? () => save(issue) : undefined}
                busy={busy === issue.id}
              />
            ))}
          </div>
          {filtered.length > limit && (
            <button
              className="civic-button"
              onClick={() => setLimit((v) => v + 20)}
            >
              Show more issues
            </button>
          )}
          {!filtered.length && (
            <div className="civic-card">
              <h2 className="text-xl font-semibold">No matching issues</h2>
              <p className="mt-2 text-text-secondary">
                Try a different topic or timing filter. Coverage may not include
                every local decision.
              </p>
              <button
                className="civic-button mt-4"
                onClick={() => {
                  setQuery('')
                  setTopic('')
                  setTiming('all')
                }}
              >
                Clear filters
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
