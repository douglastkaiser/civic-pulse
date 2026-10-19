import { test, expect } from '@playwright/test'
test.skip(
  !process.env.TEST_EMULATORS,
  'Authenticated journeys run only against local emulators.'
)
async function signUp(page, label) {
  await page.evaluate(
    async ({ email, password }) => {
      const { auth } = await import('/civic-pulse/src/lib/firebase.js')
      const { createUserWithEmailAndPassword } =
        await import('/civic-pulse/node_modules/.vite/deps/firebase_auth.js')
      await createUserWithEmailAndPassword(auth, email, password)
    },
    {
      email: `${label}-${Date.now()}@example.com`,
      password: 'Local-test-password-123!',
    }
  )
}
test('resident onboarding, saved notes, status, persistence, and account isolation', async ({
  page,
}) => {
  await page.goto('#/signin')
  await signUp(page, 'resident')
  await expect(
    page.getByRole('heading', { name: 'Make your community your priority.' })
  ).toBeVisible()
  await page.getByRole('checkbox', { name: 'Housing', exact: true }).check()
  await page
    .getByRole('combobox', { name: 'Time you have for an action' })
    .selectOption('5')
  await page.getByRole('button', { name: 'Save and see local issues' }).click()
  await expect(
    page.getByRole('heading', { name: 'Local briefing' })
  ).toBeVisible()
  await expect(
    page.getByText('Available time: 5 minutes.', { exact: false })
  ).toBeVisible()
  await page.getByRole('link', { name: 'Explore', exact: true }).click()
  await expect(
    page.getByRole('heading', { name: 'Explore your community' })
  ).toBeVisible()
  const first = page.getByRole('article').first()
  const title = await first.getByRole('heading').innerText()
  await first.getByRole('button', { name: 'Save action', exact: true }).click()
  await expect(
    first.getByRole('button', { name: 'Saved', exact: true })
  ).toBeDisabled()
  await page.getByRole('link', { name: 'Saved', exact: true }).click()
  await expect(
    page.getByRole('heading', { name: title, exact: true })
  ).toBeVisible()
  await page
    .getByRole('textbox', { name: 'Private notes' })
    .fill('Read the agenda before deciding.')
  await page.getByRole('button', { name: 'Save notes' }).click()
  await expect(page.getByText('Notes saved.', { exact: true })).toBeVisible()
  await page
    .getByRole('combobox', { name: 'Action status' })
    .selectOption('planned')
  await page.reload()
  await expect(
    page.getByRole('textbox', { name: 'Private notes' })
  ).toHaveValue('Read the agenda before deciding.')
  await expect(
    page.getByRole('combobox', { name: 'Action status' })
  ).toHaveValue('planned')
  await page
    .getByRole('combobox', { name: 'Action status' })
    .selectOption('completed')
  await page
    .getByRole('combobox', { name: 'Show', exact: true })
    .selectOption('completed')
  await expect(
    page.getByRole('heading', { name: title, exact: true })
  ).toBeVisible()
  await page.getByRole('button', { name: 'Sign out', exact: true }).click()
  await expect(
    page.getByRole('button', { name: 'Sign in with Google' })
  ).toBeVisible()
  await signUp(page, 'new-resident')
  await page.getByRole('link', { name: 'Home', exact: true }).click()
  await expect(
    page.getByRole('heading', { name: 'Make your community your priority.' })
  ).toBeVisible()
  await page.getByRole('link', { name: 'Saved', exact: true }).click()
  await expect(
    page.getByRole('heading', { name: 'Room for your next step.' })
  ).toBeVisible()
  await expect(
    page.getByRole('heading', { name: title, exact: true })
  ).toHaveCount(0)
})
test('an organization owner can create a private workspace and persist assigned actions', async ({
  page,
}) => {
  await page.goto('#/signin')
  await signUp(page, 'organizer')
  await page.getByRole('link', { name: 'Organizations', exact: true }).click()
  await page
    .getByRole('link', { name: 'Start an organization', exact: true })
    .click()
  await page
    .getByRole('textbox', { name: 'Organization name' })
    .fill('Local community group')
  await page
    .getByRole('textbox', { name: 'Mission', exact: true })
    .fill('Help residents understand and attend local public meetings.')
  await page.getByRole('button', { name: 'Create private workspace' }).click()
  await expect(
    page.getByRole('heading', { name: 'Local community group' })
  ).toBeVisible()
  await page
    .getByRole('textbox', { name: 'Action', exact: true })
    .fill('Read the next council agenda')
  await page
    .getByRole('textbox', { name: 'Campaign or goal' })
    .fill('Understand the budget')
  await page
    .getByRole('combobox', { name: 'Assign to' })
    .selectOption({ label: 'You' })
  await page.getByRole('button', { name: 'Add action', exact: true }).click()
  await expect(
    page.getByRole('heading', { name: 'Read the next council agenda' })
  ).toBeVisible()
  await page.reload()
  await expect(
    page.getByRole('heading', { name: 'Read the next council agenda' })
  ).toBeVisible()
  await expect(
    page.getByText('Assigned to you', { exact: false })
  ).toBeVisible()
})
