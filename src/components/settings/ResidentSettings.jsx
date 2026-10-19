import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  useResident,
  exportResident,
  downloadJSON,
} from '../../lib/residentStore'
import { callService } from '../../lib/service'
import Onboarding from '../Onboarding'
import DataState from '../shared/DataState'
export default function ResidentSettings({ user }) {
  const { profile, loading, error } = useResident(user.uid)
  const [message, setMessage] = useState(''),
    [failure, setFailure] = useState(null),
    [busy, setBusy] = useState(false),
    [confirm, setConfirm] = useState('')
  async function run(operation) {
    setBusy(true)
    setFailure(null)
    setMessage('')
    try {
      await operation()
    } catch (e) {
      setFailure(e.message)
    } finally {
      setBusy(false)
    }
  }
  if (loading) return <DataState loading />
  if (error) return <DataState error={error} />
  const preferences = profile?.preferences
  return (
    <section className="space-y-6 mb-10">
      <Onboarding
        key={JSON.stringify(preferences)}
        user={user}
        preferences={preferences}
        onDone={() => setMessage('Preferences saved.')}
      />
      <div className="civic-card space-y-4">
        <h2 className="text-xl font-semibold">Stay informed on your terms</h2>
        <p className="text-text-secondary text-sm">
          Email is optional. Notifications include only verified future
          deadlines. Delivery requires the notification service to be
          configured.
        </p>
        <label className="block">
          <input
            type="checkbox"
            disabled={busy || !preferences}
            checked={preferences?.weeklyDigest === true}
            onChange={(e) =>
              run(() =>
                callService('configureNotifications', {
                  weeklyDigest: e.target.checked,
                  deadlineReminders: preferences?.deadlineReminders === true,
                })
              )
            }
          />{' '}
          Weekly local deadline digest
        </label>
        <label className="block">
          <input
            type="checkbox"
            disabled={busy || !preferences}
            checked={preferences?.deadlineReminders === true}
            onChange={(e) =>
              run(() =>
                callService('configureNotifications', {
                  weeklyDigest: preferences?.weeklyDigest === true,
                  deadlineReminders: e.target.checked,
                })
              )
            }
          />{' '}
          Reminders for saved and planned actions
        </label>
      </div>
      <div className="civic-card space-y-4">
        <h2 className="text-xl font-semibold">Your information</h2>
        <p className="text-text-secondary text-sm">
          Your preferences, quiz responses, generated profile, saved actions,
          and notes belong to your account. Organization members see shared
          tasks; only explicitly published name and mission appear on your
          public organization page.
        </p>
        <button
          className="civic-button"
          disabled={busy}
          onClick={() =>
            run(async () => {
              downloadJSON(
                await exportResident(user.uid),
                'civic-pulse-my-data.json'
              )
              setMessage('Your data export is ready.')
            })
          }
        >
          Export profile and saved actions
        </button>
        <Link
          to="/profile/analysis"
          className="text-accent-blue underline block"
        >
          View optional political profile analysis
        </Link>
        <details>
          <summary className="text-accent-red cursor-pointer">
            Delete my account and private data
          </summary>
          <p className="text-sm text-text-secondary mt-3">
            This permanently deletes your profile, saved actions, notes, private
            generation history, and email subscription. Delete organizations you
            own first. Shared organization activity may remain; backup retention
            is controlled by the hosting provider.
          </p>
          <label className="block mt-3">
            Type DELETE to confirm
            <input
              className="civic-input mt-2"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              autoComplete="off"
            />
          </label>
          <button
            className="civic-button mt-3"
            disabled={busy || confirm !== 'DELETE'}
            onClick={() =>
              run(async () => {
                await callService('deleteResidentAccount')
                window.location.assign(window.location.pathname)
              })
            }
          >
            Delete permanently
          </button>
        </details>
      </div>
      {failure && (
        <p role="alert" className="text-accent-red">
          {failure}
        </p>
      )}
      {message && <p role="status">{message}</p>}
    </section>
  )
}
