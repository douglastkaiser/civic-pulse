import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../lib/auth'
import { useActions, updateAction } from '../lib/residentStore'
import { ACTION_STATES } from '../../shared/contracts.js'
import DataState from './shared/DataState'
function SavedAction({ action, uid }) {
  const [notes, setNotes] = useState(action.notes),
    [busy, setBusy] = useState(false),
    [error, setError] = useState(null),
    [undo, setUndo] = useState(null),
    [message, setMessage] = useState('')
  async function update(changes) {
    setBusy(true)
    setError(null)
    try {
      await updateAction(uid, action.id, changes)
      if (changes.state) setUndo(action.state)
      setMessage(changes.notes != null ? 'Notes saved.' : 'Action updated.')
    } catch {
      setError('Your change could not be saved. Please try again.')
    } finally {
      setBusy(false)
    }
  }
  return (
    <article className="civic-card space-y-4">
      <h2 className="text-xl font-semibold">
        <Link
          className="hover:underline"
          to={`/issues/${action.locationId}/${encodeURIComponent(action.issueId)}`}
        >
          {action.title}
        </Link>
      </h2>
      <label className="block">
        Action status
        <select
          className="civic-input mt-2"
          disabled={busy}
          value={action.state}
          onChange={(e) => update({ state: e.target.value })}
        >
          {ACTION_STATES.map((s) => (
            <option key={s} value={s}>
              {s[0].toUpperCase() + s.slice(1)}
            </option>
          ))}
        </select>
      </label>
      {undo && (
        <button
          className="text-accent-blue underline"
          disabled={busy}
          onClick={async () => {
            const previous = undo
            await update({ state: previous })
            setUndo(null)
          }}
        >
          Undo status change
        </button>
      )}
      <label className="block">
        Private notes
        <textarea
          rows={3}
          className="civic-input mt-2"
          maxLength={4000}
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
      </label>
      <div className="flex flex-wrap gap-4 items-center">
        <button
          className="civic-button"
          disabled={busy || notes === action.notes}
          onClick={() => update({ notes })}
        >
          Save notes
        </button>
        <Link
          className="text-accent-blue underline"
          to={`/issues/${action.locationId}/${encodeURIComponent(action.issueId)}`}
        >
          Check latest details and outcome
        </Link>
      </div>
      {error && (
        <p role="alert" className="text-accent-red">
          {error}
        </p>
      )}
      {message && (
        <p role="status" className="text-sm text-text-secondary">
          {message}
        </p>
      )}
    </article>
  )
}
export default function SavedPage() {
  const { user } = useAuth(),
    { actions, loading, error } = useActions(user?.uid)
  const [filter, setFilter] = useState('active')
  const visible = actions.filter(
    (a) =>
      filter === 'all' ||
      (filter === 'active'
        ? ['saved', 'planned'].includes(a.state)
        : a.state === filter)
  )
  return (
    <div className="page-wrap space-y-6">
      <header>
        <p className="eyebrow">Your own path to participation</p>
        <h1 className="text-4xl font-semibold mt-3">Saved actions</h1>
        <p className="text-text-secondary mt-3">
          Plan a next step, keep a note, and recognize what you have done.
        </p>
      </header>
      <label className="block max-w-xs">
        Show
        <select
          className="civic-input mt-2"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        >
          <option value="active">Saved and planned</option>
          <option value="completed">Completed</option>
          <option value="dismissed">Dismissed</option>
          <option value="all">All actions</option>
        </select>
      </label>
      {loading && <DataState loading />}
      {error && (
        <DataState error={error} onRetry={() => window.location.reload()} />
      )}
      <div className="grid md:grid-cols-2 gap-5">
        {visible.map((action) => (
          <SavedAction key={action.id} action={action} uid={user.uid} />
        ))}
      </div>
      {!loading && !error && !visible.length && (
        <div className="civic-card">
          <h2 className="text-xl font-semibold">Room for your next step.</h2>
          <p className="mt-2 text-text-secondary">
            {filter === 'active' || filter === 'all'
              ? 'Save an issue from Explore to start your personal action list.'
              : `No ${filter} actions yet. Change the filter to see your other actions.`}
          </p>
          <Link className="civic-button inline-block mt-4" to="/explore">
            Find a local issue
          </Link>
        </div>
      )}
    </div>
  )
}
