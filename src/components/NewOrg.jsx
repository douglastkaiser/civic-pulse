import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../lib/auth'
import { saveOrg } from '../lib/orgStore'
export default function NewOrg() {
  const { user } = useAuth(),
    navigate = useNavigate()
  const [name, setName] = useState(''),
    [mission, setMission] = useState(''),
    [busy, setBusy] = useState(false),
    [error, setError] = useState(null)
  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError(null)
    try {
      const id = crypto.randomUUID()
      await saveOrg(user.uid, {
        id,
        name: name.trim(),
        mission: mission.trim(),
        active_campaigns: [],
      })
      navigate(`/org/${id}`)
    } catch {
      setError('Your organization could not be created. Please try again.')
    } finally {
      setBusy(false)
    }
  }
  return (
    <div className="page-wrap max-w-2xl">
      <p className="eyebrow">A shared purpose, a clear next step</p>
      <h1 className="text-3xl font-semibold my-4">Start an organization</h1>
      <p className="text-text-secondary mb-6">
        Create a private workspace for your group. Invite members and choose
        what to publish when you are ready.
      </p>
      <form onSubmit={submit} className="civic-card space-y-4">
        <label className="block">
          Organization name
          <input
            className="civic-input mt-2"
            required
            maxLength={200}
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>
        <label className="block">
          Mission
          <textarea
            className="civic-input mt-2"
            rows={4}
            required
            minLength={20}
            maxLength={10000}
            value={mission}
            onChange={(e) => setMission(e.target.value)}
          />
        </label>
        {error && <p role="alert">{error}</p>}
        <button
          className="civic-button"
          disabled={busy || !name.trim() || mission.trim().length < 20}
        >
          {busy ? 'Creating…' : 'Create private workspace'}
        </button>
      </form>
    </div>
  )
}
