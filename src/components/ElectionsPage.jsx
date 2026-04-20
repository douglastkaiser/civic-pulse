import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { loadLocation, LOCATION_LABELS } from '../lib/data'
import { getDynamicLocationLabels } from '../lib/locationStore'
import BridgeBuildingPanel from './bridge/BridgeBuildingPanel'

function ElectionCard({ election }) {
  const daysUntil = election.date
    ? Math.ceil((new Date(election.date) - Date.now()) / (1000 * 60 * 60 * 24))
    : null

  return (
    <article className="bg-bg-panel border border-border rounded-lg p-4">
      <div className="flex items-start justify-between gap-3">
        <h2 className="text-base font-semibold text-text-primary">
          {election.race || election.measure || election.title}
        </h2>
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

      {election.date && (
        <div className="text-xs text-text-tertiary mt-1">
          {new Date(election.date).toLocaleDateString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            year: 'numeric',
          })}
        </div>
      )}

      {election.candidates?.length > 0 && (
        <p className="text-sm text-text-secondary mt-2">
          <span className="text-text-tertiary">Candidates:</span> {election.candidates.join(', ')}
        </p>
      )}

      {election.relevance && (
        <p className="text-sm text-accent-amber mt-2">{election.relevance}</p>
      )}

      {election.action && (
        <p className="text-sm text-accent-green mt-2">→ {election.action}</p>
      )}

      {election.bridge_building && (
        <BridgeBuildingPanel
          bridge={election.bridge_building}
          header="BRIDGE BUILDING"
          sectionTitle={election.race ? 'RACE BRIDGE FRAME' : 'MEASURE BRIDGE FRAME'}
          className="mt-3"
        />
      )}
    </article>
  )
}

export default function ElectionsPage() {
  const { locationId } = useParams()
  const [location, setLocation] = useState(null)
  const [labels, setLabels] = useState(LOCATION_LABELS)
  const [loading, setLoading] = useState(true)

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
  }, [locationId])

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
            <ElectionCard key={election.id || election.race || election.measure || election.title} election={election} />
          ))}
        </div>
      )}
    </div>
  )
}
