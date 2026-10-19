import { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useAuth } from '../lib/auth'
import { loadUserOrgs } from '../lib/orgStore'
import { callService } from '../lib/service'
import DataState from './shared/DataState'
export default function OrganizationsPage() {
  const { user } = useAuth(),
    [params, setParams] = useSearchParams()
  const [orgs, setOrgs] = useState(null),
    [error, setError] = useState(null),
    [retry, setRetry] = useState(0),
    [busy, setBusy] = useState(false)
  const invite = params.get('invite')
  useEffect(() => {
    let active = true
    setError(null)
    loadUserOrgs(user.uid)
      .then((value) => {
        if (active) setOrgs(value)
      })
      .catch(() => {
        if (active) setError('Your organizations could not be loaded.')
      })
    return () => {
      active = false
    }
  }, [user.uid, retry])
  async function accept() {
    setBusy(true)
    try {
      await callService('acceptOrganizationInvite', { token: invite })
      setParams({})
      setRetry((v) => v + 1)
    } catch (e) {
      setError(e.message)
    } finally {
      setBusy(false)
    }
  }
  return (
    <div className="page-wrap space-y-6">
      <header className="flex flex-wrap gap-4 items-center justify-between">
        <div>
          <p className="eyebrow">Work together locally</p>
          <h1 className="text-4xl font-semibold mt-3">Your organizations</h1>
        </div>
        <Link className="civic-button" to="/org/new">
          Start an organization
        </Link>
      </header>
      {invite && (
        <div className="civic-card">
          <p>
            You have an invitation. Accept it with the verified email address it
            was created for.
          </p>
          <button
            className="civic-button mt-3"
            disabled={busy}
            onClick={accept}
          >
            Accept invitation
          </button>
        </div>
      )}
      {error && (
        <DataState error={error} onRetry={() => setRetry((v) => v + 1)} />
      )}
      {!orgs && !error && <DataState loading />}
      <div className="grid md:grid-cols-2 gap-4">
        {orgs?.map((org) => (
          <Link
            className="civic-card hover:border-accent-blue"
            key={org.id}
            to={`/org/${org.id}`}
          >
            <h2 className="text-xl font-semibold">{org.name}</h2>
            <p className="text-text-secondary mt-2">{org.mission}</p>
            <p className="text-sm text-accent-green mt-4">
              {org.createdBy === user.uid ? 'Owner' : org.members?.[user.uid]}
            </p>
          </Link>
        ))}
      </div>
      {orgs?.length === 0 && (
        <p className="civic-card">
          Your groups will appear here. Start a workspace or ask an organizer
          for an invitation.
        </p>
      )}
    </div>
  )
}
