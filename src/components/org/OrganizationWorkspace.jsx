import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { collection, doc, onSnapshot } from 'firebase/firestore'
import { db } from '../../lib/firebase'
import { useAuth } from '../../lib/auth'
import { callService } from '../../lib/service'
export default function OrganizationWorkspace({ orgId }) {
  const { user } = useAuth(),
    navigate = useNavigate()
  const [org, setOrg] = useState(null),
    [tasks, setTasks] = useState([]),
    [activity, setActivity] = useState([]),
    [error, setError] = useState(null),
    [message, setMessage] = useState(''),
    [busy, setBusy] = useState(false)
  const [title, setTitle] = useState(''),
    [campaign, setCampaign] = useState(''),
    [assignee, setAssignee] = useState(''),
    [dueDate, setDue] = useState(''),
    [email, setEmail] = useState(''),
    [role, setRole] = useState('member'),
    [inviteURL, setInviteURL] = useState(''),
    [confirmDelete, setConfirmDelete] = useState(false)
  useEffect(() => {
    const fail = () =>
      setError('This workspace could not be loaded. You may not have access.')
    const unsubscribers = [
      onSnapshot(
        doc(db, 'organizations', orgId),
        (snap) => {
          if (snap.exists()) setOrg(snap.data())
          else fail()
        },
        fail
      ),
      onSnapshot(
        collection(db, 'organizations', orgId, 'tasks'),
        (snap) => setTasks(snap.docs.map((d) => ({ ...d.data(), id: d.id }))),
        fail
      ),
      onSnapshot(
        collection(db, 'organizations', orgId, 'activity'),
        (snap) =>
          setActivity(
            snap.docs
              .map((d) => d.data())
              .sort((a, b) => (b.at?.seconds || 0) - (a.at?.seconds || 0))
              .slice(0, 20)
          ),
        fail
      ),
    ]
    return () => unsubscribers.forEach((unsubscribe) => unsubscribe())
  }, [orgId])
  async function run(operation) {
    setBusy(true)
    setError(null)
    setMessage('')
    try {
      await operation()
    } catch (e) {
      setError(e.message || 'Your change could not be saved.')
    } finally {
      setBusy(false)
    }
  }
  if (!org)
    return (
      <div className="page-wrap" role={error ? 'alert' : 'status'}>
        {error || 'Loading workspace…'}
      </div>
    )
  const owner = org.createdBy === user.uid,
    editor = owner || org.members?.[user.uid] === 'organizer'
  return (
    <div className="page-wrap space-y-6">
      <header>
        <p className="eyebrow">Private organization workspace</p>
        <h1 className="text-4xl font-semibold mt-3">{org.name}</h1>
        <p className="text-text-secondary mt-3">{org.mission}</p>
      </header>
      {error && (
        <p className="text-accent-red" role="alert">
          {error}
        </p>
      )}
      {message && <p role="status">{message}</p>}
      <section className="civic-card space-y-4">
        <h2 className="text-2xl font-semibold">Campaign actions</h2>
        <p className="text-text-secondary">
          {tasks.filter((t) => t.status === 'completed').length} of{' '}
          {tasks.length} actions completed. Only workspace members can see these
          actions.
        </p>
        {editor && (
          <form
            className="grid sm:grid-cols-2 gap-3"
            onSubmit={(e) => {
              e.preventDefault()
              run(async () => {
                await callService('saveOrganizationTask', {
                  orgId,
                  taskId: crypto.randomUUID(),
                  changes: {
                    title: title.trim(),
                    campaign: campaign.trim(),
                    assignee,
                    dueDate,
                    status: 'planned',
                  },
                })
                setTitle('')
                setMessage('Action added.')
              })
            }}
          >
            <label>
              Action
              <input
                className="civic-input mt-2"
                required
                maxLength={300}
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </label>
            <label>
              Campaign or goal
              <input
                className="civic-input mt-2"
                maxLength={200}
                value={campaign}
                onChange={(e) => setCampaign(e.target.value)}
              />
            </label>
            <label>
              Assign to
              <select
                className="civic-input mt-2"
                value={assignee}
                onChange={(e) => setAssignee(e.target.value)}
              >
                <option value="">Unassigned</option>
                {(org.memberIds || [org.createdBy]).map((uid) => (
                  <option key={uid} value={uid}>
                    {uid === user.uid
                      ? 'You'
                      : org.memberLabels?.[uid] || 'Organization member'}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Due date
              <input
                className="civic-input mt-2"
                type="date"
                value={dueDate}
                onChange={(e) => setDue(e.target.value)}
              />
            </label>
            <button
              disabled={busy || !title.trim()}
              className="civic-button justify-self-start"
            >
              Add action
            </button>
          </form>
        )}
        <div className="space-y-3">
          {tasks.map((task) => (
            <div
              key={task.id}
              className="border border-border rounded-lg p-4 flex flex-wrap justify-between gap-4"
            >
              <div>
                <h3 className="font-semibold">{task.title}</h3>
                <p className="text-sm text-text-secondary">
                  {task.campaign || 'General action'} ·{' '}
                  {task.dueDate || 'No due date'} ·{' '}
                  {task.assignee === user.uid
                    ? 'Assigned to you'
                    : task.assignee
                      ? org.memberLabels?.[task.assignee] ||
                        'Organization member'
                      : 'Unassigned'}
                </p>
              </div>
              <label className="min-w-40">
                Status
                <select
                  className="civic-input mt-1"
                  aria-label={`Status for ${task.title}`}
                  disabled={!editor || busy}
                  value={task.status}
                  onChange={(e) =>
                    run(() =>
                      callService('saveOrganizationTask', {
                        orgId,
                        taskId: task.id,
                        changes: { status: e.target.value },
                      })
                    )
                  }
                >
                  <option value="planned">Planned</option>
                  <option value="in_progress">In progress</option>
                  <option value="completed">Completed</option>
                </select>
              </label>
            </div>
          ))}
        </div>
        {!tasks.length && (
          <p className="text-text-secondary">
            No actions yet. Add a goal and one concrete next step.
          </p>
        )}
      </section>
      <section className="civic-card space-y-4">
        <h2 className="text-2xl font-semibold">Members and roles</h2>
        {Object.entries(org.members || { [org.createdBy]: 'owner' }).map(
          ([uid, memberRole]) => (
            <div key={uid} className="flex flex-wrap items-center gap-3">
              <span className="text-sm break-all flex-1">
                {uid === user.uid
                  ? 'You'
                  : org.memberLabels?.[uid] || 'Organization member'}
              </span>
              {owner && memberRole !== 'owner' ? (
                <select
                  className="civic-input max-w-40"
                  aria-label={`Role for ${org.memberLabels?.[uid] || 'organization member'}`}
                  disabled={busy}
                  value={memberRole}
                  onChange={(e) =>
                    run(() =>
                      callService('manageOrganization', {
                        operation: 'role',
                        orgId,
                        uid,
                        role: e.target.value,
                      })
                    )
                  }
                >
                  <option value="member">Member</option>
                  <option value="organizer">Organizer</option>
                </select>
              ) : (
                <span>{memberRole}</span>
              )}
              {owner && memberRole !== 'owner' && (
                <button
                  className="text-accent-red underline"
                  disabled={busy}
                  onClick={() =>
                    run(() =>
                      callService('manageOrganization', {
                        operation: 'remove',
                        orgId,
                        uid,
                      })
                    )
                  }
                >
                  Remove
                </button>
              )}
            </div>
          )
        )}
        {owner && (
          <form
            className="space-y-3 border-t border-border pt-4"
            onSubmit={(e) => {
              e.preventDefault()
              run(async () => {
                const response = await callService('createOrganizationInvite', {
                  orgId,
                  email,
                  role,
                })
                setInviteURL(
                  `${window.location.origin}${window.location.pathname}#/organizations?invite=${response.token}`
                )
                setMessage(
                  'Invitation created. Share the link with the intended recipient; it expires in 7 days.'
                )
              })
            }}
          >
            <label className="block">
              Invite by verified email
              <input
                className="civic-input mt-2"
                required
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </label>
            <label className="block">
              Invite role
              <select
                className="civic-input mt-2"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="member">Member</option>
                <option value="organizer">Organizer</option>
              </select>
            </label>
            <button className="civic-button" disabled={busy}>
              Create invitation link
            </button>
            {inviteURL && (
              <label className="block">
                Share this private invitation
                <input
                  readOnly
                  className="civic-input mt-2"
                  value={inviteURL}
                  onFocus={(e) => e.target.select()}
                />
              </label>
            )}
          </form>
        )}
      </section>
      {owner && (
        <section className="civic-card space-y-4">
          <h2 className="text-2xl font-semibold">Public page</h2>
          <p className="text-text-secondary">
            Publishing shares your organization’s name and mission. Member
            identities, notes, and campaign tasks stay private.
          </p>
          <div className="flex flex-wrap gap-3">
            <button
              className="civic-button"
              disabled={busy}
              onClick={() =>
                run(async () => {
                  await callService('manageOrganization', {
                    operation: 'publish',
                    orgId,
                  })
                  setMessage('Public page published.')
                })
              }
            >
              Publish name and mission
            </button>
            <button
              className="text-accent-red underline"
              disabled={busy}
              onClick={() =>
                run(async () => {
                  await callService('manageOrganization', {
                    operation: 'unpublish',
                    orgId,
                  })
                  setMessage('Public page unpublished.')
                })
              }
            >
              Unpublish
            </button>
            <Link
              className="text-accent-blue underline"
              to={`/org/${orgId}/public`}
            >
              View public page
            </Link>
          </div>
          <details>
            <summary className="cursor-pointer text-accent-red">
              Delete organization
            </summary>
            <p className="mt-3 text-text-secondary">
              This permanently removes the workspace, tasks, invites, and public
              page.
            </p>
            <label className="block my-3">
              <input
                type="checkbox"
                checked={confirmDelete}
                onChange={(e) => setConfirmDelete(e.target.checked)}
              />{' '}
              I understand this cannot be undone.
            </label>
            <button
              disabled={busy || !confirmDelete}
              className="civic-button"
              onClick={() =>
                run(async () => {
                  await callService('manageOrganization', {
                    operation: 'delete',
                    orgId,
                  })
                  navigate('/organizations')
                })
              }
            >
              Delete permanently
            </button>
          </details>
        </section>
      )}
      <section className="civic-card">
        <h2 className="text-2xl font-semibold mb-4">Workspace activity</h2>
        {activity.length ? (
          <ul className="space-y-2 text-sm text-text-secondary">
            {activity.map((event, index) => (
              <li key={index}>
                {event.operation} ·{' '}
                {event.at?.toDate?.().toLocaleString() || 'Just now'}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-text-secondary">
            Activity will appear as the workspace changes.
          </p>
        )}
      </section>
    </div>
  )
}
