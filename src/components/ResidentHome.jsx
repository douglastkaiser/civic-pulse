import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../lib/auth'
import { useResident, useActions, saveAction } from '../lib/residentStore'
import { loadIssues } from '../lib/data'
import {
  JURISDICTIONS,
  coverageLabel,
  sourceAge,
  issueDeadline,
  relevance,
  isCurrentIssue,
  opportunityTime,
} from '../lib/civic'
import Onboarding from './Onboarding'
import IssueCard from './IssueCard'
import DataState from './shared/DataState'
export default function ResidentHome({ demo = false }) {
  const { user } = useAuth()
  const resident = useResident(demo ? undefined : user?.uid)
  const { actions, error: actionError } = useActions(
    demo ? undefined : user?.uid
  )
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [retry, setRetry] = useState(0)
  const [busy, setBusy] = useState(null)
  const demoPreferences = {
    locationId: JURISDICTIONS[0].id,
    interests: ['Housing', 'Transportation'],
    availableMinutes: 15,
  }
  const locationId = demo
    ? demoPreferences.locationId
    : resident.profile?.preferences?.locationId
  useEffect(() => {
    setData(null)
    setError(null)
    if (!locationId) return
    const controller = new AbortController()
    loadIssues(locationId, { signal: controller.signal })
      .then(setData)
      .catch(() => {
        if (!controller.signal.aborted)
          setError('Local issues could not be loaded.')
      })
    return () => controller.abort()
  }, [locationId, retry])
  if (resident.loading) return <DataState loading />
  if (resident.error)
    return (
      <DataState
        error={resident.error}
        onRetry={() => window.location.reload()}
      />
    )
  if (!locationId)
    return (
      <div className="page-wrap">
        <Onboarding user={user} />
      </div>
    )
  const preferences = demo ? demoPreferences : resident.profile.preferences
  const jurisdiction = JURISDICTIONS.find((j) => j.id === locationId)
  const current = (data?.issues || []).filter((i) => isCurrentIssue(i))
  const recommended = [...current]
    .sort(
      (a, b) =>
        (a.provenance === 'source_record' ? 0 : 1) -
          (b.provenance === 'source_record' ? 0 : 1) ||
        relevance(b, preferences).score - relevance(a, preferences).score
    )
    .slice(0, 4)
  const deadlines = current
    .filter((i) => opportunityTime(i))
    .sort(
      (a, b) => Date.parse(opportunityTime(a)) - Date.parse(opportunityTime(b))
    )
    .slice(0, 3)
  async function save(issue) {
    setBusy(issue.id)
    try {
      await saveAction(user.uid, locationId, issue)
    } catch {
      setError('This action could not be saved. Please try again.')
    } finally {
      setBusy(null)
    }
  }
  return (
    <div className="page-wrap space-y-4">
      {demo && (
        <div className="desk-notice">
          <p className="font-semibold">Example resident briefing</p>
          <p className="text-sm text-text-secondary mt-1">
            This demo follows housing and transportation in Austin with 15
            minutes available.{' '}
            <Link className="underline" to="/signin">
              Sign in to choose your own priorities.
            </Link>
          </p>
        </div>
      )}
      <header className="flex flex-wrap justify-between gap-4">
        <div>
          <p className="eyebrow">Your local briefing · {jurisdiction?.label}</p>
          <h1 className="text-4xl font-semibold mt-3">Local briefing</h1>
          <p className="text-text-secondary mt-3">
            Available time: {preferences.availableMinutes} minutes. Choose a
            local issue to follow.
          </p>
        </div>
        <Link className="text-accent-blue underline self-start" to="/settings">
          Change your interests
        </Link>
      </header>
      <div className="desk-notice">
        <p className="font-medium">{coverageLabel(locationId)}</p>
        <p className="text-sm text-text-secondary mt-1">
          {sourceAge(data)}. Confirm current details with the original source.
        </p>
      </div>
      {(error || actionError) && (
        <DataState
          error={error || actionError}
          onRetry={() => setRetry((v) => v + 1)}
        />
      )}
      {!data && !error && <DataState loading />}
      {data && (
        <div className="briefing-grid">
          <section className="briefing-panel">
            <div className="flex justify-between items-baseline gap-3 mb-4">
              <h2 className="text-2xl font-semibold">
                Upcoming meetings and deadlines
              </h2>
              <Link
                className="text-accent-blue underline"
                to={`/explore?location=${locationId}`}
              >
                Explore all issues
              </Link>
            </div>
            {deadlines.length ? (
              <div className="issue-list">
                {deadlines.map((issue) => (
                  <IssueCard
                    key={issue.id}
                    issue={issue}
                    locationId={locationId}
                    preferences={preferences}
                    saved={actions.some(
                      (a) =>
                        a.locationId === locationId && a.issueId === issue.id
                    )}
                    onSave={demo ? undefined : () => save(issue)}
                    busy={busy === issue.id}
                  />
                ))}
              </div>
            ) : (
              <div className="civic-card text-text-secondary">
                No verified upcoming participation dates are available for this
                area. You can still explore and follow issues.
              </div>
            )}
          </section>
          <section className="briefing-panel">
            <h2 className="text-2xl font-semibold mb-4">
              Worth your attention
            </h2>
            {recommended.length ? (
              <div className="issue-list">
                {recommended.map((issue) => (
                  <IssueCard
                    key={issue.id}
                    issue={issue}
                    locationId={locationId}
                    preferences={preferences}
                    saved={actions.some(
                      (a) =>
                        a.locationId === locationId && a.issueId === issue.id
                    )}
                    onSave={demo ? undefined : () => save(issue)}
                    busy={busy === issue.id}
                  />
                ))}
              </div>
            ) : (
              <div className="civic-card">
                No current decisions are confirmed.{' '}
                <Link
                  className="text-accent-blue underline"
                  to={`/explore?location=${locationId}`}
                >
                  Browse the archive
                </Link>{' '}
                or check back after a source update.
              </div>
            )}
          </section>
        </div>
      )}
      <section className="civic-card flex flex-wrap justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold">Keep your next step close.</h2>
          <p className="text-text-secondary mt-2">
            {
              actions.filter((a) => ['saved', 'planned'].includes(a.state))
                .length
            }{' '}
            actions waiting ·{' '}
            {actions.filter((a) => a.state === 'completed').length} completed
          </p>
        </div>
        <Link className="civic-button self-center" to="/saved">
          Open saved actions
        </Link>
      </section>
    </div>
  )
}
