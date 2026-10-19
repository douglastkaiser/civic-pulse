import { test, before } from 'node:test'
import assert from 'node:assert/strict'
import { initializeApp } from 'firebase-admin/app'
import { getFirestore } from 'firebase-admin/firestore'
import { getAuth } from 'firebase-admin/auth'
const project = 'demo-civic-pulse',
  endpoint = `http://127.0.0.1:5001/${project}/us-central1`
let db, owner, member, outsider, orgId
async function account(label) {
  const email = `${label}-${Date.now()}@example.com`,
    password = 'Test-only-password-123!'
  const response = await fetch(
    'http://127.0.0.1:9099/identitytoolkit.googleapis.com/v1/accounts:signUp?key=demo',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, returnSecureToken: true }),
    }
  )
  const user = await response.json()
  assert.ok(user.localId, JSON.stringify(user))
  await getAuth().updateUser(user.localId, { emailVerified: true })
  const refreshed = await fetch(
    'http://127.0.0.1:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=demo',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, returnSecureToken: true }),
    }
  ).then((r) => r.json())
  return { uid: user.localId, email, token: refreshed.idToken }
}
async function call(name, user, data) {
  return fetch(`${endpoint}/${name}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(user ? { Authorization: `Bearer ${user.token}` } : {}),
    },
    body: JSON.stringify({ data }),
  }).then((r) => r.json())
}
before(async () => {
  assert.ok(process.env.FIRESTORE_EMULATOR_HOST, 'Only run against emulators')
  initializeApp({ projectId: project })
  db = getFirestore()
  owner = await account('owner')
  member = await account('member')
  outsider = await account('outsider')
  orgId = `integration-${Date.now()}`
  await db
    .doc(`organizations/${orgId}`)
    .set({
      name: 'Local action group',
      mission: 'Coordinate a useful local action',
      createdBy: owner.uid,
      memberIds: [owner.uid],
      members: { [owner.uid]: 'owner' },
      privateNotes: 'Must never be public',
    })
})
test('server enforces invitation identity, roles, and public field projection', async () => {
  assert.equal(
    (
      await call('manageOrganization', outsider, {
        operation: 'publish',
        orgId,
      })
    ).error.status,
    'PERMISSION_DENIED'
  )
  const created = await call('createOrganizationInvite', owner, {
    orgId,
    email: member.email,
    role: 'member',
  })
  assert.ok(created.result?.token, JSON.stringify(created))
  const token = created.result.token
  assert.equal(
    (await call('acceptOrganizationInvite', outsider, { token })).error.status,
    'PERMISSION_DENIED'
  )
  assert.equal(
    (await call('acceptOrganizationInvite', member, { token })).result.ok,
    true
  )
  assert.equal(
    (await call('acceptOrganizationInvite', member, { token })).error.status,
    'PERMISSION_DENIED'
  )
  assert.equal(
    (
      await call('manageOrganization', member, {
        operation: 'role',
        orgId,
        uid: member.uid,
        role: 'organizer',
      })
    ).error.status,
    'PERMISSION_DENIED'
  )
  assert.equal(
    (
      await call('manageOrganization', owner, {
        operation: 'role',
        orgId,
        uid: member.uid,
        role: 'organizer',
      })
    ).result.ok,
    true
  )
  assert.equal(
    (await db.doc(`organizations/${orgId}`).get()).data().members[member.uid],
    'organizer'
  )
  const task = {
    title: 'Read the agenda',
    assignee: member.uid,
    campaign: 'Budget',
    dueDate: '2026-11-01',
    status: 'planned',
  }
  assert.equal(
    (await call('saveOrganizationTask', outsider, { orgId, changes: task }))
      .error.status,
    'PERMISSION_DENIED'
  )
  const saved = await call('saveOrganizationTask', member, {
    orgId,
    changes: task,
  })
  assert.ok(saved.result?.taskId, JSON.stringify(saved))
  assert.equal(
    (
      await db.doc(`organizations/${orgId}/tasks/${saved.result.taskId}`).get()
    ).data().title,
    task.title
  )
  assert.equal(
    (
      await call('saveOrganizationTask', owner, {
        orgId,
        changes: { ...task, assignee: outsider.uid },
      })
    ).error.status,
    'INVALID_ARGUMENT'
  )
  assert.equal(
    (await call('manageOrganization', owner, { operation: 'publish', orgId }))
      .result.ok,
    true
  )
  const published = (await db.doc(`publicOrganizations/${orgId}`).get()).data()
  assert.equal(published.name, 'Local action group')
  assert.equal(published.privateNotes, undefined)
  assert.equal(published.members, undefined)
  assert.equal(
    (await call('manageOrganization', owner, { operation: 'unpublish', orgId }))
      .result.ok,
    true
  )
  assert.equal(
    (await db.doc(`publicOrganizations/${orgId}`).get()).exists,
    false
  )
})
test('notifications require explicit opt-in and unsubscribe disables all delivery', async () => {
  await db
    .doc(`users/${member.uid}`)
    .set({ preferences: { locationId: 'austin-78702' } })
  const result = await call('configureNotifications', member, {
    weeklyDigest: true,
    deadlineReminders: true,
  })
  assert.equal(result.result?.ok, true, JSON.stringify(result))
  const subscribers = await db
    .collection('notificationSubscribers')
    .where('uid', '==', member.uid)
    .get()
  const token = subscribers.docs[0].data().unsubscribeToken
  const response = await fetch(
    `${endpoint}/unsubscribeNotifications?token=${token}`,
    { method: 'POST' }
  )
  assert.equal(response.status, 200)
  const preferences = (await db.doc(`users/${member.uid}`).get()).data()
    .preferences
  assert.equal(preferences.weeklyDigest, false)
  assert.equal(preferences.deadlineReminders, false)
})
test('account deletion prevents orphan owners and removes private subcollections', async () => {
  assert.equal(
    (await call('deleteResidentAccount', owner, {})).error.status,
    'FAILED_PRECONDITION'
  )
  await db
    .doc(`users/${member.uid}/actions/test`)
    .set({ title: 'Private note' })
  assert.equal(
    (await call('deleteResidentAccount', member, {})).result.ok,
    true
  )
  assert.equal(
    (await db.doc(`users/${member.uid}/actions/test`).get()).exists,
    false
  )
  assert.equal(
    (await db.doc(`organizations/${orgId}`).get())
      .data()
      .memberIds.includes(member.uid),
    false
  )
  await call('manageOrganization', owner, { operation: 'delete', orgId })
  assert.equal((await call('deleteResidentAccount', owner, {})).result.ok, true)
  await getAuth().deleteUser(outsider.uid)
})
