# Civic Pulse

Civic Pulse helps residents understand local decisions, choose a useful next step, and coordinate with community organizations.

## What works in this upgrade

- Compact neo-retro layout with persistent, independent color and font presets in Appearance settings.
- Public issue browsing, search, topic/timing filters, source links, an explicit demo, and coverage and archive labels.
- Resident onboarding with a location, interests, and available time; the political quiz is optional.
- Private saved/planned/completed/dismissed actions, persistent notes, and personal data export.
- Calendar export only for verified upcoming dates, plus a local editable comment draft.
- Private organization workspaces, campaign actions and assignments, roles, email-bound invitation links, and deliberately published name/mission pages.
- Authenticated server-side AI generation with validation and per-user usage limits. Browser-stored provider keys are removed.
- Opt-in verified-deadline notification jobs, unsubscribe, and recent-sign-in account deletion.
- A validated source pipeline with truthful collection health and last-known-good preservation.

## Development

Node 22+, Python 3.12, and Java 21 are used by the checks.

```sh
npm ci
pip install -r scripts/requirements.txt
npm run dev
```

Copy `.env.example` to `.env.local` for staging configuration or local emulator selection. The Firebase web configuration is public configuration, not a provider credential. Provider secrets belong in Firebase Secret Manager.

```sh
npm run check
npm run test:rules
npm run test:integration
npx playwright install chromium
npm run test:resident
```

`npm run test:resident` runs anonymous and authenticated browser journeys against the isolated demo emulators. `npm run test:browser` runs the anonymous browser tests without emulators.

## Data and deployment

`shared/jurisdictions.json` is the shared coverage registry. Austin has a partial configured Legistar connector. Orange County is an archived snapshot without an automated source. Existing archive content is not newly verified by this upgrade.

```sh
python scripts/pipeline.py
python scripts/pipeline.py austin-78702
python scripts/pipeline.py --scrape-only
```

The pipeline collects official records without private profiles or AI scoring. Failed collection preserves existing issue data, records a failure, and exits nonzero. New jurisdictions require tested connectors; requesting coverage does not create civic facts using AI.

The frontend remains a static React/Vite app hosted on GitHub Pages. Firebase rules and Functions must be staged and deployed separately before releasing server-backed workflows. See [the operations guide](docs/OPERATIONS.md) for configuration, validation, migration, rollout, and remaining release work. [The upgrade plan](UPGRADE_PLAN.md) records implementation status and outstanding product milestones.
