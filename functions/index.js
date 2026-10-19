import { initializeApp } from 'firebase-admin/app'
import { getAuth } from 'firebase-admin/auth'
import { getFirestore, FieldValue } from 'firebase-admin/firestore'
import { onCall, onRequest, HttpsError } from 'firebase-functions/v2/https'
import { onSchedule } from 'firebase-functions/v2/scheduler'
import { defineSecret, defineString } from 'firebase-functions/params'
import { createHash, randomBytes, randomUUID } from 'node:crypto'
import { SYSTEM_PROMPT } from '../shared/profilePrompt.js'
import { validateGeneratedProfile } from '../shared/contracts.js'
import {
  reserveGeneration,
  publicOrganization,
  validInvite,
  notificationCandidates,
} from './policy.js'
initializeApp()
const db = getFirestore()
const anthropicKey = defineSecret('ANTHROPIC_API_KEY')
const emailKey = defineSecret('RESEND_API_KEY')
const appURL = defineString('APP_URL', {
  default: 'https://douglastkaiser.github.io/civic-pulse/',
})
const mailFrom = defineString('MAIL_FROM', { default: '' })
const unsubscribeURL = defineString('UNSUBSCRIBE_URL', { default: '' })
const sha = (value) => createHash('sha256').update(value).digest('hex')
const options = { region: 'us-central1', maxInstances: 5, timeoutSeconds: 120 }
function uidOf(request) {
  if (!request.auth)
    throw new HttpsError('unauthenticated', 'Sign in to continue.')
  return request.auth.uid
}
function text(value, max) {
  if (typeof value !== 'string' || !value.trim() || value.length > max)
    throw new HttpsError('invalid-argument', 'Invalid request field.')
  return value.trim()
}
function organizationId(value) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,100}$/.test(value))
    throw new HttpsError('invalid-argument', 'Invalid organization ID.')
  return value
}
async function ownedOrg(request, orgId) {
  const uid = uidOf(request),
    ref = db.doc(`organizations/${organizationId(orgId)}`),
    snap = await ref.get()
  if (!snap.exists || snap.data().createdBy !== uid)
    throw new HttpsError(
      'permission-denied',
      'Only the organization owner can do this.'
    )
  return { uid, ref, org: snap.data() }
}
async function audit(ref, operation, uid) {
  await ref
    .collection('activity')
    .add({ operation, actor: uid, at: FieldValue.serverTimestamp() })
}

export const generateResidentProfile = onCall(
  { ...options, secrets: [anthropicKey] },
  async (request) => {
    const uid = uidOf(request),
      requestId = text(request.data?.requestId, 100)
    if (!request.auth.token.email_verified)
      throw new HttpsError(
        'permission-denied',
        'A verified email is required for AI generation.'
      )
    if (!/^[a-zA-Z0-9-]{16,100}$/.test(requestId))
      throw new HttpsError('invalid-argument', 'Invalid request ID.')
    const quiz = request.data?.quizAnswers
    if (!quiz || typeof quiz !== 'object' || Array.isArray(quiz))
      throw new HttpsError('invalid-argument', 'Quiz answers are required.')
    const serialized = JSON.stringify(quiz)
    if (serialized.length > 12000)
      throw new HttpsError('invalid-argument', 'Quiz responses are too long.')
    const jobRef = db.doc(`users/${uid}/aiJobs/${requestId}`),
      usageRef = db.doc(`users/${uid}/system/aiUsage`)
    const reservation = await db.runTransaction(async (tx) => {
      const [job, usage] = await Promise.all([tx.get(jobRef), tx.get(usageRef)])
      if (job.exists) {
        if (job.data().status === 'completed') return job.data().result
        throw new HttpsError(
          'already-exists',
          'This request is already processing or failed. Start a new request if needed.'
        )
      }
      const date = new Date().toISOString()
      let next
      try {
        next = reserveGeneration(
          usage.data() || {},
          date.slice(0, 10),
          date.slice(0, 7)
        )
      } catch {
        throw new HttpsError(
          'resource-exhausted',
          'Your generation limit has been reached.'
        )
      }
      tx.set(usageRef, next)
      tx.set(jobRef, {
        status: 'processing',
        createdAt: FieldValue.serverTimestamp(),
      })
      return null
    })
    if (reservation) return reservation
    try {
      // One upstream attempt per reservation; retrying billable requests can duplicate cost.
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        signal: AbortSignal.timeout(75000),
        headers: {
          'content-type': 'application/json',
          'x-api-key': anthropicKey.value(),
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: 'claude-haiku-4-5-20251001',
          max_tokens: 8192,
          system: SYSTEM_PROMPT,
          messages: [{ role: 'user', content: serialized }],
        }),
      })
      if (!response.ok) throw new Error('Upstream unavailable')
      const result = await response.json()
      const content =
        result.content
          ?.filter((b) => b.type === 'text')
          .map((b) => b.text)
          .join('') || ''
      const profile = validateGeneratedProfile(
        JSON.parse(
          content.replace(/^\s*```(?:json)?\s*/, '').replace(/\s*```\s*$/, '')
        )
      )
      const allowed = Object.fromEntries(
        [
          'manifesto',
          'political_compass',
          'political_positions',
          'values',
          'issue_salience',
          'political_context',
        ].map((k) => [k, profile[k]])
      )
      await jobRef.set(
        {
          status: 'completed',
          result: allowed,
          usage: result.usage || {},
          finishedAt: FieldValue.serverTimestamp(),
        },
        { merge: true }
      )
      return allowed
    } catch {
      await jobRef.set(
        { status: 'failed', finishedAt: FieldValue.serverTimestamp() },
        { merge: true }
      )
      throw new HttpsError(
        'unavailable',
        'Profile generation could not finish. Your existing profile has been preserved.'
      )
    }
  }
)

export const createOrganizationInvite = onCall(options, async (request) => {
  const { uid, ref } = await ownedOrg(request, request.data?.orgId)
  const email = text(request.data.email, 254).toLowerCase(),
    role = request.data.role
  if (
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ||
    !['organizer', 'member'].includes(role)
  )
    throw new HttpsError('invalid-argument', 'Invalid invitation.')
  const token = randomBytes(32).toString('hex')
  await db.doc(`organizationInvites/${sha(token)}`).set({
    orgId: ref.id,
    invitedBy: uid,
    email,
    role,
    expiresAt: Date.now() + 7 * 86400000,
  })
  await audit(ref, 'Invitation created', uid)
  return { token }
})
export const acceptOrganizationInvite = onCall(options, async (request) => {
  const uid = uidOf(request),
    token = text(request.data?.token, 100)
  if (!request.auth.token.email_verified || !request.auth.token.email)
    throw new HttpsError('permission-denied', 'A verified email is required.')
  await db.runTransaction(async (tx) => {
    const inviteRef = db.doc(`organizationInvites/${sha(token)}`),
      invite = await tx.get(inviteRef)
    if (!validInvite(invite.data(), request.auth.token.email, Date.now()))
      throw new HttpsError(
        'permission-denied',
        'This invitation is invalid, expired, or for a different email.'
      )
    const value = invite.data(),
      orgRef = db.doc(`organizations/${value.orgId}`),
      org = await tx.get(orgRef)
    if (!org.exists)
      throw new HttpsError('not-found', 'Organization not found.')
    if (org.data().createdBy !== value.invitedBy)
      throw new HttpsError(
        'permission-denied',
        'Invitation is no longer valid.'
      )
    if (org.data().createdBy === uid || org.data().members?.[uid])
      throw new HttpsError(
        'already-exists',
        'You already belong to this organization.'
      )
    tx.update(orgRef, {
      members: {
        ...org.data().members,
        [org.data().createdBy]: 'owner',
        [uid]: value.role,
      },
      memberIds: [
        ...new Set([
          org.data().createdBy,
          ...(org.data().memberIds || []),
          uid,
        ]),
      ],
      memberLabels: {
        ...org.data().memberLabels,
        [uid]: request.auth.token.name || request.auth.token.email,
      },
      updatedAt: FieldValue.serverTimestamp(),
    })
    tx.update(inviteRef, {
      acceptedBy: uid,
      acceptedAt: FieldValue.serverTimestamp(),
    })
    tx.set(orgRef.collection('activity').doc(), {
      operation: 'Member joined',
      actor: uid,
      at: FieldValue.serverTimestamp(),
    })
  })
  return { ok: true }
})
export const manageOrganization = onCall(options, async (request) => {
  const { uid, ref, org } = await ownedOrg(request, request.data?.orgId)
  const operation = request.data.operation
  if (operation === 'publish')
    await db.doc(`publicOrganizations/${ref.id}`).set({
      ...publicOrganization(org),
      publishedAt: FieldValue.serverTimestamp(),
    })
  else if (operation === 'unpublish')
    await db.doc(`publicOrganizations/${ref.id}`).delete()
  else if (operation === 'delete') {
    await db.doc(`publicOrganizations/${ref.id}`).delete()
    const invites = await db
      .collection('organizationInvites')
      .where('orgId', '==', ref.id)
      .get()
    for (const invite of invites.docs) await invite.ref.delete()
    await db.recursiveDelete(ref)
    return { ok: true }
  } else if (operation === 'role' || operation === 'remove') {
    const member = text(request.data.uid, 128)
    if (member === uid)
      throw new HttpsError(
        'failed-precondition',
        'The owner cannot be removed or demoted.'
      )
    if (
      operation === 'role' &&
      !['organizer', 'member'].includes(request.data.role)
    )
      throw new HttpsError('invalid-argument', 'Invalid role.')
    await db.runTransaction(async (tx) => {
      const snapshot = await tx.get(ref),
        current = snapshot.data()
      if (!current || current.createdBy !== uid || !current.members?.[member])
        throw new HttpsError('not-found', 'Member not found.')
      const members = { ...current.members }
      const memberLabels = { ...current.memberLabels }
      if (operation === 'remove') {
        delete members[member]
        delete memberLabels[member]
      } else members[member] = request.data.role
      tx.update(ref, {
        members,
        memberLabels,
        memberIds: Object.keys(members),
        updatedAt: FieldValue.serverTimestamp(),
      })
    })
  } else throw new HttpsError('invalid-argument', 'Unknown operation.')
  await audit(ref, `Organization ${operation}`, uid)
  return { ok: true }
})
export const saveOrganizationTask = onCall(options, async (request) => {
  const uid = uidOf(request),
    orgId = organizationId(request.data?.orgId)
  const taskId = request.data.taskId || randomUUID()
  if (!/^[a-zA-Z0-9-]{1,100}$/.test(taskId))
    throw new HttpsError('invalid-argument', 'Invalid task ID.')
  const orgRef = db.doc(`organizations/${orgId}`),
    taskRef = orgRef.collection('tasks').doc(taskId)
  await db.runTransaction(async (tx) => {
    const [orgSnapshot, taskSnapshot] = await Promise.all([
      tx.get(orgRef),
      tx.get(taskRef),
    ])
    const org = orgSnapshot.data()
    if (!org || (org.createdBy !== uid && org.members?.[uid] !== 'organizer'))
      throw new HttpsError(
        'permission-denied',
        'Only owners and organizers can edit campaign actions.'
      )
    const members = { ...org.members, [org.createdBy]: 'owner' }
    const memberIds = Object.keys(members)
    const changes = request.data.changes || {}
    const allowed = Object.fromEntries(
      ['title', 'campaign', 'assignee', 'dueDate', 'status']
        .filter((k) => k in changes)
        .map((k) => [k, changes[k]])
    )
    const task = {
      ...(taskSnapshot.data() || {
        assignee: '',
        campaign: '',
        dueDate: '',
        status: 'planned',
        createdBy: uid,
      }),
      ...allowed,
    }
    task.title = text(task.title, 300)
    if (
      typeof task.campaign !== 'string' ||
      task.campaign.length > 200 ||
      typeof task.dueDate !== 'string' ||
      (task.dueDate !== '' && !/^\d{4}-\d\d-\d\d$/.test(task.dueDate)) ||
      !['planned', 'in_progress', 'completed'].includes(task.status) ||
      (task.assignee !== '' && !memberIds.includes(task.assignee))
    )
      throw new HttpsError('invalid-argument', 'Invalid campaign action.')
    if (
      !org.members?.[org.createdBy] ||
      !org.memberIds?.includes(org.createdBy)
    )
      tx.update(orgRef, { members, memberIds })
    tx.set(taskRef, { ...task, updatedAt: FieldValue.serverTimestamp() })
    tx.set(orgRef.collection('activity').doc(), {
      operation: taskSnapshot.exists
        ? 'Campaign action updated'
        : 'Campaign action created',
      actor: uid,
      taskId,
      at: FieldValue.serverTimestamp(),
    })
  })
  return { taskId }
})
export const deleteResidentAccount = onCall(options, async (request) => {
  const uid = uidOf(request)
  if (Date.now() / 1000 - request.auth.token.auth_time > 300)
    throw new HttpsError(
      'failed-precondition',
      'Sign out and sign in again before deleting your account.'
    )
  const owned = await db
    .collection('organizations')
    .where('createdBy', '==', uid)
    .limit(1)
    .get()
  if (!owned.empty)
    throw new HttpsError(
      'failed-precondition',
      'Delete the organizations you own before deleting your account.'
    )
  const member = await db
    .collection('organizations')
    .where('memberIds', 'array-contains', uid)
    .get()
  for (const org of member.docs) {
    await db.runTransaction(async (tx) => {
      const snap = await tx.get(org.ref)
      const data = snap.data()
      if (!data) return
      const members = { ...data.members }
      const memberLabels = { ...data.memberLabels }
      delete members[uid]
      delete memberLabels[uid]
      tx.update(org.ref, {
        members,
        memberLabels,
        memberIds: Object.keys(members),
      })
    })
  }
  const requests = await db
    .collection('coverageRequests')
    .where('uid', '==', uid)
    .get()
  for (const record of requests.docs) await record.ref.delete()
  for (const field of ['invitedBy', 'acceptedBy']) {
    const invites = await db
      .collection('organizationInvites')
      .where(field, '==', uid)
      .get()
    for (const invite of invites.docs) await invite.ref.delete()
  }
  if (request.auth.token.email) {
    const invites = await db
      .collection('organizationInvites')
      .where('email', '==', request.auth.token.email.toLowerCase())
      .get()
    for (const invite of invites.docs) await invite.ref.delete()
  }
  await db.doc(`notificationSubscribers/${sha(uid)}`).delete()
  await db.recursiveDelete(db.doc(`users/${uid}`))
  await getAuth().deleteUser(uid)
  return { ok: true }
})

export const configureNotifications = onCall(options, async (request) => {
  const uid = uidOf(request)
  if (!request.auth.token.email_verified)
    throw new HttpsError(
      'permission-denied',
      'Verify your email to enable notifications.'
    )
  const weeklyDigest = request.data?.weeklyDigest === true,
    deadlineReminders = request.data?.deadlineReminders === true
  const token = randomBytes(32).toString('hex')
  await db.doc(`notificationSubscribers/${sha(uid)}`).set({
    uid,
    email: request.auth.token.email,
    weeklyDigest,
    deadlineReminders,
    unsubscribeHash: sha(token),
    unsubscribeToken: token,
  })
  await db
    .doc(`users/${uid}`)
    .set({ preferences: { weeklyDigest, deadlineReminders } }, { merge: true })
  return { ok: true }
})
export const unsubscribeNotifications = onRequest(
  options,
  async (request, response) => {
    const token = String(request.query.token || '')
    if (!/^[a-f0-9]{64}$/.test(token)) {
      response.status(400).send('Invalid unsubscribe link.')
      return
    }
    if (request.method === 'GET') {
      response
        .set('Content-Type', 'text/html')
        .send(
          `<form method="POST"><p>Unsubscribe from Civic Pulse email notifications?</p><button>Unsubscribe</button></form>`
        )
      return
    }
    if (request.method !== 'POST') {
      response.status(405).send('Method not allowed')
      return
    }
    const found = await db
      .collection('notificationSubscribers')
      .where('unsubscribeHash', '==', sha(token))
      .get()
    for (const sub of found.docs) {
      await db
        .doc(`users/${sub.data().uid}`)
        .set(
          { preferences: { weeklyDigest: false, deadlineReminders: false } },
          { merge: true }
        )
      await sub.ref.delete()
    }
    response.send('You have been unsubscribed.')
  }
)
export const sendCivicNotifications = onSchedule(
  {
    schedule: 'every day 09:00',
    timeZone: 'America/Los_Angeles',
    secrets: [emailKey],
    ...options,
  },
  async () => {
    if (!mailFrom.value() || !unsubscribeURL.value()) return
    const subscribers = await db.collection('notificationSubscribers').get()
    const today = new Date().toISOString().slice(0, 10),
      monday = new Date().getUTCDay() === 1
    for (const subscriber of subscribers.docs) {
      const sub = subscriber.data()
      const profile = (await db.doc(`users/${sub.uid}`).get()).data()
      if (!profile?.preferences?.locationId) continue
      const response = await fetch(
        `${appURL.value()}data/issues/${encodeURIComponent(profile.preferences.locationId)}.json`,
        { signal: AbortSignal.timeout(15000) }
      )
      if (!response.ok) continue
      const data = await response.json()
      const candidates = notificationCandidates(data.issues || [], Date.now())
      const actions = await db.collection(`users/${sub.uid}/actions`).get()
      const followed = new Set(
        actions.docs
          .filter(
            (d) =>
              ['saved', 'planned'].includes(d.data().state) &&
              d.data().locationId === profile.preferences.locationId
          )
          .map((d) => d.data().issueId)
      )
      const selected = candidates.filter(
        (i) =>
          (monday && sub.weeklyDigest && profile.preferences.weeklyDigest) ||
          (sub.deadlineReminders &&
            profile.preferences.deadlineReminders &&
            followed.has(i.id) &&
            Date.parse(i.public_comment.deadline) - Date.now() <= 48 * 3600000)
      )
      if (!selected.length) continue
      const key = sha(`${sub.uid}:${today}`),
        job = db.doc(`users/${sub.uid}/deliveries/${key}`)
      const acquired = await db.runTransaction(async (tx) => {
        const snap = await tx.get(job)
        if (
          snap.exists &&
          (snap.data().status === 'sent' || snap.data().leaseUntil > Date.now())
        )
          return false
        tx.set(job, { status: 'sending', leaseUntil: Date.now() + 120000 })
        return true
      })
      if (!acquired) continue
      const unsubscribe = `${unsubscribeURL.value()}?token=${sub.unsubscribeToken}`
      const result = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        signal: AbortSignal.timeout(30000),
        headers: {
          Authorization: `Bearer ${emailKey.value()}`,
          'Content-Type': 'application/json',
          'Idempotency-Key': key,
        },
        body: JSON.stringify({
          from: mailFrom.value(),
          to: [sub.email],
          subject: 'Your Civic Pulse local deadlines',
          text:
            selected
              .map(
                (i) =>
                  `${i.title}\nDeadline: ${i.public_comment.deadline}\nVerify details: ${i.public_comment.source_url}`
              )
              .join('\n\n') +
            `\n\nReview saved actions: ${appURL.value()}#/saved\nUnsubscribe: ${unsubscribe}`,
        }),
      })
      if (!result.ok) throw new Error('Notification delivery failed')
      await job.set({
        status: 'sent',
        sentAt: FieldValue.serverTimestamp(),
        leaseUntil: 0,
      })
    }
  }
)
