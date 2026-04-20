import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { loadLocation, LOCATION_LABELS, ORG_IDS_BY_LOCATION, loadOrg } from '../lib/data'
import { getDynamicLocationLabels } from '../lib/locationStore'

function formatElectionDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

function RaceCard({ election, followedOrgIndex }) {
  const daysUntil = election.date
    ? Math.ceil((new Date(election.date) - Date.now()) / (1000 * 60 * 60 * 24))
    : null

  const associatedOrgs = Array.isArray(election.associated_organizations)
    ? election.associated_organizations
    : []

  const relevantFollowedOrgs = associatedOrgs
    .filter((org) => org.applicability !== 'not_directly_applicable')
    .map((org) => {
      const fallbackName = org.name || org.org_id || 'Unknown organization'
      const followedOrg = org.org_id ? followedOrgIndex[org.org_id] : null
      return {
        ...org,
        displayName: followedOrg?.name || fallbackName,
      }
    })

  const notDirectlyApplicableOrgs = associatedOrgs
    .filter((org) => org.applicability === 'not_directly_applicable')
    .map((org) => ({
      ...org,
      displayName: followedOrgIndex[org.org_id]?.name || org.name || org.org_id || 'Unknown organization',
    }))

  const bridge = election.bridge_building || {}

  return (
    <article className="bg-bg-panel border border-border rounded-lg p-4 space-y-3">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h2 className="text-base font-semibold text-text-primary">
            {election.race || election.measure || election.title}
          </h2>
          {election.race_identifier && (
            <p className="text-xs font-mono text-text-tertiary mt-1">ID: {election.race_identifier}</p>
          )}
          {election.date && <div className="text-xs text-text-tertiary mt-1">{formatElectionDate(election.date)}</div>}
        </div>
        {daysUntil !== null && (
          <span
            className={`text-xs font-mono whitespace-nowrap px-2 py-1 rounded ${
              daysUntil <= 30
                ? 'bg-accent-red/15 text-accent-red'
                : daysUntil <= 90
                  ? 'bg-accent-amber/15 text-accent-amber'
                  : 'bg-accent-blue/15 text-accent-blue'
            }`}
          >
            {daysUntil > 0 ? `${daysUntil}d` : 'Today'}
          </span>
        )}
      </div>

      {election.candidates?.length > 0 && (
        <p className="text-sm text-text-secondary">
          <span className="text-text-tertiary">Candidates:</span> {election.candidates.join(', ')}
        </p>
      )}

      {election.relevance && <p className="text-sm text-accent-amber">{election.relevance}</p>}

      {election.action && <p className="text-sm text-accent-green">→ {election.action}</p>}

      <section className="border border-border rounded bg-bg-elevated p-3">
        <h3 className="font-mono text-xs font-bold text-text-tertiary tracking-wide mb-2">RELEVANT FOLLOWED ORGS</h3>
        {relevantFollowedOrgs.length === 0 ? (
          <p className="text-xs text-text-tertiary">No followed organizations mapped to this race yet.</p>
        ) : (
          <ul className="space-y-1.5">
            {relevantFollowedOrgs.map((org) => (
              <li key={`${election.race_identifier || election.race}-${org.org_id || org.displayName}`} className="text-xs text-text-secondary">
                <span className="text-text-primary font-medium">{org.displayName}</span>
                {org.relevance_note ? <span className="text-text-tertiary"> — {org.relevance_note}</span> : null}
              </li>
            ))}
          </ul>
        )}

        {notDirectlyApplicableOrgs.length > 0 && (
          <div className="mt-2 pt-2 border-t border-border/70">
            <p className="text-[11px] font-mono text-text-tertiary mb-1">NOT DIRECTLY APPLICABLE</p>
            <ul className="space-y-1">
              {notDirectlyApplicableOrgs.map((org) => (
                <li key={`${election.race_identifier || election.race}-na-${org.org_id || org.displayName}`} className="text-xs text-text-tertiary">
                  <span>{org.displayName}</span>
                  {org.relevance_note ? <span> — {org.relevance_note}</span> : null}
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>

      {(bridge.why_this_race_matters_to_everyone || bridge.shared_stakes || bridge.anti_tribal_framing) && (
        <section className="border border-border rounded bg-bg-elevated p-3">
          <h3 className="font-mono text-xs font-bold text-text-tertiary tracking-wide mb-2">SHARED STAKES BRIDGE CONTENT</h3>
          {bridge.why_this_race_matters_to_everyone && (
            <p className="text-xs text-text-secondary mb-2">
              <span className="text-text-primary font-medium">Why this race matters to everyone:</span>{' '}
              {bridge.why_this_race_matters_to_everyone}
            </p>
          )}
          {bridge.shared_stakes && (
            <p className="text-xs text-text-secondary mb-2">
              <span className="text-text-primary font-medium">Shared stakes:</span> {bridge.shared_stakes}
            </p>
          )}
          {bridge.anti_tribal_framing && (
            <p className="text-xs text-text-secondary">
              <span className="text-text-primary font-medium">Anti-tribal framing:</span> {bridge.anti_tribal_framing}
            </p>
          )}
        </section>
      )}
    </article>
  )
}

export default function ElectionsPage() {
  const { locationId } = useParams()
  const [location, setLocation] = useState(null)
  const [labels, setLabels] = useState(LOCATION_LABELS)
  const [loading, setLoading] = useState(true)
  const [followedOrgs, setFollowedOrgs] = useState([])

  useEffect(() => {
    getDynamicLocationLabels()
      .then((dynamic) => setLabels({ ...LOCATION_LABELS, ...dynamic }))
      .catch(() => setLabels(LOCATION_LABELS))
  }, [])

  useEffect(() => {
    if (!locationId) return

    setLoading(true)
    loadLocation(locationId)
      .then((loc) => setLocation(loc))
      .catch((err) => {
        console.error('Failed to load elections:', err)
        setLocation(null)
      })
      .finally(() => setLoading(false))

    const orgIds = ORG_IDS_BY_LOCATION[locationId] || []
    if (orgIds.length === 0) {
      setFollowedOrgs([])
      return
    }

    Promise.all(orgIds.map((id) => loadOrg(id).catch(() => null))).then((orgs) => {
      setFollowedOrgs(orgs.filter(Boolean))
    })
  }, [locationId])

  const followedOrgIndex = useMemo(
    () => Object.fromEntries(followedOrgs.map((org) => [org.id, org])),
    [followedOrgs],
  )

  const locationLabel = labels[locationId] || locationId
  const elections = location?.upcoming_elections || []

  if (loading) {
    return (
      <div className="h-full p-4 animate-pulse">
        <div className="h-6 w-48 bg-bg-elevated rounded mb-6" />
        <div className="space-y-3">
          <div className="h-28 bg-bg-elevated rounded" />
          <div className="h-28 bg-bg-elevated rounded" />
        </div>
      </div>
    )
  }

  return (
    <div className="h-full p-4 overflow-auto animate-fade-in">
      <div className="flex items-center justify-between gap-3 mb-4">
        <div>
          <h1 className="font-mono text-lg font-bold text-text-primary tracking-wide">🗳️ ELECTIONS</h1>
          <p className="text-sm text-text-secondary">{locationLabel}</p>
        </div>
        <div className="flex items-center gap-2 flex-wrap justify-end">
          {Object.entries(labels).map(([id, label]) => (
            <Link
              key={id}
              to={`/elections/${id}`}
              className={`text-xs font-mono px-2 py-1 rounded border transition-colors ${
                id === locationId
                  ? 'border-accent-blue/40 bg-accent-blue/15 text-accent-blue'
                  : 'border-border text-text-tertiary hover:text-text-secondary'
              }`}
            >
              {label}
            </Link>
          ))}
        </div>
      </div>

      {elections.length === 0 ? (
        <div className="bg-bg-panel border border-border rounded-lg p-6 text-center">
          <p className="text-text-secondary">No upcoming elections found for this location yet.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {elections.map((election) => (
            <RaceCard
              key={election.race_identifier || election.id || election.race || election.measure || election.title}
              election={election}
              followedOrgIndex={followedOrgIndex}
            />
          ))}
        </div>
      )}
    </div>
  )
}
