import { test, before, after, beforeEach } from 'node:test'
import { readFileSync } from 'node:fs'
import {
  initializeTestEnvironment,
  assertSucceeds,
  assertFails,
} from '@firebase/rules-unit-testing'
import {
  doc,
  setDoc,
  getDoc,
  updateDoc,
  collection,
  query,
  where,
  getDocs,
} from 'firebase/firestore'
let env
before(async () => {
  env = await initializeTestEnvironment({
    projectId: 'demo-civic-pulse',
    firestore: {
      rules: readFileSync('firestore.rules', 'utf8'),
      host: '127.0.0.1',
      port: 8080,
    },
  })
})
after(async () => env?.cleanup())
beforeEach(async () => env.clearFirestore())
const org = {
  name: 'Group',
  mission: 'A shared purpose',
  createdBy: 'alice',
  memberIds: ['alice'],
  members: { alice: 'owner' },
}
test('profiles and actions are private, including list reads', async () => {
  const alice = env.authenticatedContext('alice').firestore(),
    bob = env.authenticatedContext('bob').firestore(),
    anonymous = env.unauthenticatedContext().firestore()
  await assertSucceeds(
    setDoc(doc(alice, 'users/alice'), { display_name: 'Alice' })
  )
  await assertFails(getDoc(doc(bob, 'users/alice')))
  await assertFails(getDoc(doc(anonymous, 'users/alice')))
  const action = {
    schema_version: 1,
    issueId: 'one',
    locationId: 'austin',
    title: 'A decision',
    state: 'saved',
    notes: '',
  }
  await assertSucceeds(setDoc(doc(alice, 'users/alice/actions/one'), action))
  await assertFails(getDocs(collection(bob, 'users/alice/actions')))
  await assertFails(setDoc(doc(bob, 'users/alice/actions/one'), action))
  await assertFails(
    updateDoc(doc(alice, 'users/alice/actions/one'), { state: 'invalid' })
  )
  await assertFails(
    setDoc(doc(alice, 'users/alice/system/aiUsage'), { daily: 0 })
  )
})
test('organizations require membership and prevent self-escalation', async () => {
  const alice = env.authenticatedContext('alice').firestore(),
    bob = env.authenticatedContext('bob').firestore()
  await assertSucceeds(setDoc(doc(alice, 'organizations/group'), org))
  await assertFails(getDoc(doc(bob, 'organizations/group')))
  await assertFails(
    updateDoc(doc(bob, 'organizations/group'), {
      members: { alice: 'owner', bob: 'owner' },
      memberIds: ['alice', 'bob'],
    })
  )
  await assertFails(
    updateDoc(doc(alice, 'organizations/group'), { createdBy: 'bob' })
  )
  await env.withSecurityRulesDisabled(async (ctx) =>
    updateDoc(doc(ctx.firestore(), 'organizations/group'), {
      members: { alice: 'owner', bob: 'member' },
      memberIds: ['alice', 'bob'],
    })
  )
  await assertSucceeds(getDoc(doc(bob, 'organizations/group')))
  await assertSucceeds(
    getDocs(
      query(
        collection(bob, 'organizations'),
        where('memberIds', 'array-contains', 'bob')
      )
    )
  )
  const task = {
    title: 'Attend meeting',
    assignee: 'bob',
    dueDate: '',
    status: 'planned',
    campaign: 'Budget',
    createdBy: 'alice',
  }
  await assertFails(setDoc(doc(alice, 'organizations/group/tasks/one'), task))
  await env.withSecurityRulesDisabled((ctx) =>
    setDoc(doc(ctx.firestore(), 'organizations/group/tasks/one'), task)
  )
  await assertFails(
    updateDoc(doc(bob, 'organizations/group/tasks/one'), {
      status: 'completed',
    })
  )
})
test('publishing and shared civic data are server-controlled', async () => {
  const alice = env.authenticatedContext('alice').firestore(),
    anonymous = env.unauthenticatedContext().firestore()
  await assertFails(
    setDoc(doc(alice, 'locations/austin'), { title: 'Invented' })
  )
  await assertFails(
    setDoc(doc(alice, 'publicOrganizations/group'), { name: 'Published?' })
  )
  await env.withSecurityRulesDisabled(async (ctx) =>
    setDoc(doc(ctx.firestore(), 'publicOrganizations/group'), {
      name: 'Public',
      mission: 'Purpose',
    })
  )
  await assertSucceeds(getDoc(doc(anonymous, 'publicOrganizations/group')))
})
