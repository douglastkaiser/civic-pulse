import { test, expect } from '@playwright/test'
test('anonymous visitor can browse, search, read a source, and see honest deadlines', async ({
  page,
}) => {
  await page.goto('#/explore')
  await expect(
    page.getByRole('heading', { name: 'Explore your community' })
  ).toBeVisible()
  await expect(page.getByRole('article').first()).toBeVisible()
  await page.getByRole('searchbox', { name: 'Search' }).fill('zz-no-match')
  await expect(
    page.getByRole('heading', { name: 'No matching issues' })
  ).toBeVisible()
  await page.getByRole('button', { name: 'Clear filters' }).click()
  await page
    .getByRole('article')
    .filter({
      has: page.getByRole('link', { name: 'Original source', exact: false }),
    })
    .first()
    .getByRole('link', { name: 'Understand this issue' })
    .click()
  await expect(
    page.getByRole('heading', { name: 'What is happening' })
  ).toBeVisible()
  await expect(
    page.getByRole('link', { name: 'Read the original source' })
  ).toBeVisible()
  await expect(
    page.getByRole('button', { name: 'Add to calendar' })
  ).toHaveCount(0)
})
test('mobile filters and navigation fit a narrow viewport', async ({
  page,
}) => {
  await page.setViewportSize({ width: 360, height: 780 })
  await page.goto('#/explore')
  await expect(page.getByRole('article').first()).toBeVisible()
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth
    )
  ).toBe(true)
  await page
    .getByRole('combobox', { name: 'Area', exact: true })
    .selectOption('orange-92868')
  await expect(
    page.getByText('Archived snapshot · automatic updates unavailable', {
      exact: false,
    })
  ).toBeVisible()
  await expect(page.getByRole('article').first()).toBeVisible()
})
test('unknown routes recover and sign in protects private actions', async ({
  page,
}) => {
  await page.goto('#/unknown')
  await expect(
    page.getByRole('heading', { name: 'Page not found' })
  ).toBeVisible()
  await page.goto('#/saved')
  await expect(
    page.getByRole('button', { name: 'Sign in with Google' })
  ).toBeVisible()
})
test('a verified future meeting offers a usable calendar download', async ({
  page,
}) => {
  const now = new Date(),
    future = new Date(Date.now() + 86400000)
  await page.route('**/data/issues/austin-78702.json', (route) =>
    route.fulfill({
      json: {
        schema_version: 1,
        last_successful_fetch_at: now.toISOString(),
        issues: [
          {
            schema_version: 1,
            id: 'verified-meeting',
            title: 'Council meeting',
            summary: 'Review the official agenda.',
            policy_domains: [],
            source_url: 'https://example.gov/meeting',
            provenance: 'source_record',
            status: 'upcoming',
            meeting: {
              verified: true,
              verified_at: now.toISOString(),
              starts_at: future.toISOString(),
              timezone: 'America/Chicago',
              source_url: 'https://example.gov/meeting',
            },
          },
        ],
      },
    })
  )
  await page.goto('#/issues/austin-78702/verified-meeting')
  const downloadPromise = page.waitForEvent('download')
  await page.getByRole('button', { name: 'Add to calendar' }).click()
  const download = await downloadPromise
  expect(download.suggestedFilename()).toBe('civic-pulse-event.ics')
})

test('the explicit demo uses example preferences without requiring a personal profile', async ({
  page,
}) => {
  await page.goto('#/demo')
  await expect(
    page.getByText('Example resident briefing', { exact: true })
  ).toBeVisible()
  await expect(
    page.getByRole('heading', { name: 'Local briefing' })
  ).toBeVisible()
  await expect(
    page.getByText('This demo follows housing and transportation', {
      exact: false,
    })
  ).toBeVisible()
})

test('appearance presets and fonts persist without changing the compact layout', async ({
  page,
}) => {
  await page.goto('#/appearance')
  await expect(
    page.getByRole('heading', { name: 'Appearance settings' })
  ).toBeVisible()
  await page.getByLabel('Color theme', { exact: true }).selectOption('darkplus')
  await expect(page.locator('.app-shell')).toHaveCSS(
    'background-color',
    'rgb(30, 30, 30)'
  )
  await expect(page.locator('.app-shell')).toHaveCSS(
    'color',
    'rgb(222, 222, 222)'
  )
  await page
    .getByLabel('Interface font', { exact: true })
    .selectOption('courier')
  await expect(page.getByRole('button', { name: /Dark\+/ })).toHaveAttribute(
    'aria-pressed',
    'true'
  )
  await page.reload()
  await expect(page.getByLabel('Color theme', { exact: true })).toHaveValue(
    'darkplus'
  )
  await expect(page.getByLabel('Interface font', { exact: true })).toHaveValue(
    'courier'
  )
  await page
    .getByRole('link', { name: 'Example briefing', exact: true })
    .click()
  await expect(page.getByRole('article').first()).toBeVisible()
  const appearance = await page
    .getByRole('article')
    .first()
    .evaluate((element) => ({
      radius: getComputedStyle(element).borderRadius,
      font: getComputedStyle(element).fontFamily,
    }))
  expect(appearance.radius).toBe('0px')
  expect(appearance.font).toContain('Courier New')
  await page.setViewportSize({ width: 360, height: 780 })
  await page.getByRole('link', { name: 'Appearance', exact: true }).click()
  await expect(page.getByLabel('Color theme', { exact: true })).toBeVisible()
  await page.getByLabel('Color theme', { exact: true }).selectOption('retro90s')
  await page.getByLabel('Interface font', { exact: true }).selectOption('mono')
})
