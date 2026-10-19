# Civic Pulse operations and release guide

The upgrade is implemented in the working tree. Local tests and their recorded outcomes are listed in `UPGRADE_PLAN.md`. Live Firebase rules, paid AI calls, email delivery, and a resident/organization pilot require the deployment environment and have not been represented as verified.

## Architecture

- React/Vite frontend remains deployable to GitHub Pages, with route-level code splitting and public browsing. Hash routes preserve Pages compatibility.
- `shared/jurisdictions.json` is the coverage registry used by the client and Python pipeline. Austin has a partial `austintexas` Legistar connector; Orange County is explicitly an archived snapshot without automatic collection.
- Python publishes validated civic records and raw source snapshots atomically. It never sends private profiles to a public data pipeline. Existing files are preserved on errors and successful empty windows.
- Firestore `users/{uid}` and `actions` are private. AI jobs, usage reservations, and delivery records are server-owned subcollections. Organizations have private members and tasks. Public pages read a separate allowlisted snapshot.
- Firebase Functions provide authenticated AI, invitation acceptance, organization publishing and membership changes, account cleanup, opt-in notification configuration, and scheduled delivery.

## Local checks

Use Node 22 or later, Python 3.12, and Java 21 for the Firestore emulator.

```sh
npm ci
pip install -r scripts/requirements.txt
npm run check
npm run test:rules
npm run test:integration
npx playwright install chromium
npm run test:browser
npm run test:resident
```

On constrained cloud workspaces, point tool caches to writable directories using `npm --cache`, `PLAYWRIGHT_BROWSERS_PATH`, `FIREBASE_EMULATORS_PATH`, and `XDG_CONFIG_HOME`. Use `NO_PROXY=127.0.0.1,localhost` for local emulator access while preserving the configured outbound proxy.

For development with the isolated `demo-civic-pulse` project, set `VITE_USE_EMULATORS=true` in `.env.local` and start:

```sh
npx firebase emulators:start --project demo-civic-pulse --only auth,firestore,functions
npm run dev
```

The demo project cannot call production Firebase services. Never use real provider credentials in emulator tests. Tests that require AI output should inject a fake provider in the test process rather than call the paid API.

## Staged rollout

1. Select a staging Firebase project and inspect its existing deployed rules and legacy documents. The checkout does not contain credentials to inspect production rules. Export a backup before schema migration or a production rules change.
2. Configure Firebase web settings for the staging project using the `VITE_FIREBASE_*` fields in `.env.example`. Configure allowed auth domains for staging and production origins.
3. Deploy `firestore.rules` and functions to staging. Run the permission suite and authenticated resident/organization browser tests against emulators before doing this. Existing organization documents need `members` and `memberIds` fields; owner-only reads remain backward compatible, but invitations require a membership migration.
4. Set `ANTHROPIC_API_KEY` as a Firebase secret. Set `APP_URL` to the frontend base URL, including its trailing slash. AI uses an authenticated callable endpoint; browsers no longer store or send provider API keys.
5. For email, configure the `RESEND_API_KEY` secret, verified `MAIL_FROM`, and the deployed `UNSUBSCRIBE_URL` function URL. The scheduled job stays quiet without sender/unsubscribe configuration or eligible verified future deadlines. Confirm one delivery and an unsubscribe with a consenting test address.
6. Deploy functions, rules, then the frontend. Production deployment is a separate action from local implementation. Review the project's billing plan and region before enabling scheduled functions and provider calls.
7. Run one source collection against Austin, review source timestamps and links, and compare a small sample with official agendas. Do not label Orange County as live until a tested connector exists.
8. Pilot with residents and one organization. Confirm mobile usability, source accuracy, private/public boundaries, successful calendar import, and the complete action lifecycle before broad rollout.

Firebase deploy commands, once the intended project is authenticated and staged:

```sh
npx firebase deploy --project YOUR_STAGING_PROJECT --only firestore:rules,firestore:indexes,functions
```

No production project alias or default deploy target is supplied, to avoid accidental deployment to the existing project.

## Data contracts and source failures

`schema_version: 1` is required for new normalized records. Runtime validators reject malformed collections and duplicate IDs. Compatibility readers accept existing unversioned snapshots, clearly labeled as unverified archive data. The Orange County legacy format was migrated with deterministic IDs; no new facts or verification dates were added.

Pipeline status is `updated`, `no_changes`, `failed`, or `unsupported`. `last_attempt_at` advances for attempts; `last_successful_fetch_at` advances only after both matter and event collection and validation succeed. Per-record `fetched_at` is retained for older records. No AI-generation timestamp is written for source-only records. `needs_rescrape` remains a boolean.

The connector has date-window filtering, pagination, retry bounds, stable external IDs, and source-local time zones. Ambiguous local times remain unverified. Source facts and unverified legacy analysis remain distinguishable. Only exact reviewed statuses (Passed, Adopted, Failed, Rejected, Postponed, Withdrawn, and Agenda Ready) map to application states; unknown source statuses remain unresolved. Extend mappings per connector with fixtures.

Failed runs exit nonzero and preserve existing issue data. The Actions workflow commits failure health metadata, but does not deploy a failed pipeline run. A subsequent successful run publishes it. Monitor Actions failures; choose an operational owner before launch.

## AI limits and privacy

Per-account reservations allow five generations/day and USD 2/month, reserving USD 0.08 per attempt. Reservations are conservative and are not refunded on failures. These limits assume the configured Haiku model and present token pricing; revisit the reservation when changing model or pricing. Set an organization-level provider budget as an additional cost control. One billable upstream attempt is made per job. Request IDs prevent the same reservation from being executed twice; users may start a fresh request after a failed job.

Requests are limited to 12,000 characters and 8,192 output tokens, time out, and must pass profile validation. Only allowlisted profile fields return to the browser. Political quiz answers must not be added to analytics, console logs, or incident reports.

Users can export their profile and saved actions. Account deletion requires recent sign-in, removes private subcollections and notification configuration, and prevents leaving ownerless organizations. Shared organization activity and provider-managed backups may persist; establish a retention policy before launch. Server job results and usage records currently remain until account deletion; a shorter retention job is still needed for production policy.

## Notifications

Email requires explicit opt-in and a verified account email. Deadline reminders apply to saved/planned issues in the resident's chosen area. Only source-verified, unexpired deadlines verified within the last seven days are eligible. Canceled/passed/rejected issues are suppressed. Delivery leases and provider idempotency keys prevent duplicate delivery on immediate retries. Settings and unsubscribe both disable future delivery. The first digest implementation includes verified deadlines; broader issue-change/outcome digests remain future work.

The job currently scans subscribers daily. Add pagination/batching or a queue before increasing subscriber volume. Provider idempotency retention and reconciliation should be reviewed before relying on retries beyond one day.

## Remaining release work

- Confirm live source accuracy, deployed rules, Firebase credentials and project billing, provider pricing, actual email delivery, and mobile accessibility with real users.
- Add outcome/source review tooling and connector ownership. Expansion requires fixtures, source documentation, health checks, and an accurate coverage label.
- Add followed-topic subscriptions beyond preference-based ranking, richer issue-change/outcome notifications, richer campaign goals, and aggregate organization reports.
- Add privacy-conscious operational dashboards, backup/retention schedules, feature flags, and measured performance targets after a pilot baseline.
- Native apps and broad geographic expansion remain deferred as specified in the plan.

## Verified source smoke check

The Austin collector was run successfully during implementation against `https://webapi.legistar.com/v1/austintexas`. It collected 182 recently modified matters and five meeting entries. Raw source records are retained under `public/data/sources/austin-78702.json`; normalized records are in the corresponding issues file. This is a point-in-time collection, not a guarantee of ongoing completeness. Calendar entries were normalized from their published local times; no public comment deadline or availability was inferred from a meeting alone.

## Local verification result

The completed local run passed 33 automated tests: 12 JavaScript unit/policy/contract tests, 8 Python pipeline tests, 3 Firestore permission tests, 3 callable integration tests, and 7 browser journeys. Lint, progressive type checking, data validation, the production build, and whitespace checks also passed. Emulator metadata/auth-trigger warnings did not cause failures in the asserted behaviors. Actual provider delivery and production rules remain unverified.
