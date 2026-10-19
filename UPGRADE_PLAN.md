# Civic Pulse upgrade plan

Draft based on a source review on October 18, 2026. The roadmap below is retained for context; implementation progress and release limitations are recorded at the end.

## Product direction

Make Civic Pulse the place a resident goes to understand what is changing locally, decide what matters to them, and take a useful action in the time they have available.

Confirmed audience: serve both residents and community organizations, with residents as the starting point. Build organization coordination on the same trusted civic data.

The core journey should be:

1. Choose a supported location, interests, and available time.
2. See a short list of relevant, current decisions and deadlines.
3. Understand the facts, sources, competing perspectives, and why an item was recommended.
4. Save an item, prepare a comment, contact the right office, or add a meeting to a calendar.
5. Return to see what changed and what happened after the decision.

## What the source review found

There is useful groundwork: React and Vite, Firebase authentication and Firestore, local issue and official views, elections, organization pages, themes, exports, and some provenance components. Preserve and improve these incrementally.

| Finding | Evidence | Implication |
| --- | --- | --- |
| A user without a completed manifesto can see a fixed profile | `PersonalDashboard.jsx` falls back to `PROFILE_ID`, defined as `doug` in `data.js` | Build a genuine first-use experience and make sample data an explicit demo |
| Freshness can imply success after unsuccessful collection | `pipeline.py` advances scrape timestamps when no records arrive; caught scraper failures can become empty lists; `update_freshness` converts boolean `True` values to timestamps, including flags | Separate attempts, successful checks, source changes, failures, and stale data |
| Supported locations differ between pipeline and UI | UI lists Austin and Orange County; pipeline's default locations include Austin and four other places, but not Orange County | Establish one jurisdiction registry with explicit coverage status |
| Frontend and pipeline use different freshness structures | Sidebar prefers `locations`; pipeline writes `profiles` | Adopt and validate a shared contract |
| AI requests run in the browser | Generator modules call Anthropic directly; API keys are reversibly obfuscated in local storage | Move generation behind an authenticated service with cost controls |
| Authorization cannot be verified from this checkout | Firestore stores organizations and shared locations; no Firestore rules or emulator tests were found | Inspect deployed rules and establish tested access boundaries before adding collaboration |
| Recommendations are largely presented as content | `NextStepsPanel.jsx` displays steps without a persisted action lifecycle | Add saving, reminders, completion, and outcome tracking |
| Some empty states require developer actions | Issue feed and next steps refer users to running the pipeline | Provide understandable coverage, retry, and notification flows |
| Engineering checks are minimal in the repository | Package scripts include dev/build/preview, with no lint/typecheck/test scripts | Establish CI checks for core journeys, data integrity, and permissions |

Build verification was attempted but blocked by this environment: Vite configuration calls `execSync('git rev-parse --short HEAD')`, which failed with `EPERM`. This does not establish that the deployed build is broken. No authenticated browser walkthrough or live Firebase rules inspection has been performed.

## Phase 1 — Trustworthy foundations

**Outcome:** users see their own information, know what is current, and can rely on the app when services fail.

- Replace automatic sample-profile fallback with onboarding. Offer a clearly labeled demo separately.
- Define shared, versioned schemas for jurisdictions, source records, issues, deadlines, profiles, actions, and freshness. Validate data at ingestion and application boundaries.
- Create one jurisdiction registry for frontend navigation and pipeline scheduling. Expose supported, partial, unavailable, and stale coverage honestly.
- Fix pipeline status reporting. Distinguish a successful check with no changes from collection failure, unsupported sources, and generation failure. Preserve the last known good records on failure.
- Record `last_attempt_at`, `last_successful_fetch_at`, `source_updated_at` when available, `last_successful_generation_at`, and a typed status with error details. Advance each timestamp only for the operation it describes.
- Implement source date filtering, pagination, stable external IDs, deduplication, bounded retries, and explicit source time zones. The existing date-window parameters are currently unused.
- Keep source facts separate from AI summaries and personal relevance. Require source references for actionable dates and instructions. Treat missing evidence as unknown.
- Move AI generation to an authenticated server function or service. Add request limits, timeouts, output validation, bounded retries, usage tracking, and per-user spending limits. Remove browser key persistence and migrate existing settings.
- Review deployed Firestore rules. Add ownership checks for profiles, explicit organization permissions, and separate public documents from private member data. Define who may publish shared location information.
- Add recoverable loading/error states, auth error handling, unknown-route handling, and structured error monitoring without logging political profiles or credentials.
- Add CI for linting, progressive type checking, production builds, schema validation, pipeline failure cases, and Firebase emulator access tests. Make build metadata work without requiring a Git checkout.

**Completion criteria:** a new account never inherits another profile; denied access is tested; a failed scrape cannot appear as a successful refresh; invalid AI output cannot replace valid data; one supported jurisdiction works end to end with traceable source records.

## Phase 2 — A clear, modern resident experience

**Outcome:** someone can find a relevant local decision and understand their next step on a phone.

- Build a short onboarding flow: location, interests, available time, notification preferences. Make the political quiz and manifesto optional enrichment.
- Make the home screen a weekly briefing with three primary sections: upcoming deadlines, recommended actions, and changes to followed issues.
- Use a simpler navigation structure: Home, Explore, Saved, and Profile; provide a clear location switcher. Add Organizations prominently if organization users become the primary audience.
- Redesign issue details around: what is happening, why it matters, when the decision happens, who decides, sources, and available actions. Put charts and ideological analysis in secondary views.
- Add issue search and filters for topic, jurisdiction, decision status, deadline, and effort. Retain useful existing sorting.
- Refresh the current design system with readable typography, consistent spacing, clear action buttons, restrained color, and layouts that work at narrow widths and enlarged text.
- Improve keyboard navigation, focus visibility, modal focus management, screen reader labels, contrast, reduced motion, and touch targets. Provide text alternatives for charts.
- Make public information browseable without an account where appropriate; request sign-in when someone saves or personalizes content.
- Explain empty states in user terms: no upcoming decisions, coverage unavailable, source temporarily unavailable, or no matching filters.

**Completion criteria:** representative residents can find a relevant upcoming decision and its source without assistance; core screens work at 360px width and 200% text zoom; onboarding, search, issue details, and saving work by keyboard.

## Phase 3 — Turn insight into useful action

**Outcome:** users can follow through and see the results.

- Add followed topics/issues and a persisted personal action list with saved, planned, completed, and dismissed states. Allow undo and user notes.
- Offer calendar export for verified meeting times and deadlines, including time zone, source, and update/cancellation information.
- Show verified official contact routes and public comment instructions. Clearly handle deadlines that have passed or cannot be confirmed.
- Offer editable, source-grounded comment preparation with explicit user review. Any submission or outbound communication requires a deliberate user action.
- Explain recommendations using stated interests, geography, urgency, and effort. Let users adjust priorities or dismiss recommendations; avoid unsupported numerical claims of influence.
- Add an opt-in weekly digest and selected deadline reminders with unsubscribe and notification controls. Suppress expired or unverified action prompts.
- Track issue changes and outcomes: amended, postponed, passed, rejected, or unresolved. Notify followers when a meaningful update occurs.
- Provide profile/data export and account deletion covering private stored data, with clear retention information.

**Completion criteria:** a user can discover an issue, save an action, receive an opted-in reminder, complete or dismiss it, and later see a sourced outcome; reminder jobs avoid duplicates and respect deadlines and preferences.

## Phase 4 — Organization coordination and wider coverage

**Outcome:** groups coordinate around the same reliable records, with clear permissions.

- Add invitations and owner, organizer, and member roles with tested read/write permissions.
- Turn existing campaign and engagement views into persisted workflows: campaign goals, assigned actions, due dates, progress, and an activity history.
- Add deliberate publishing controls for public organization pages. Keep member profiles and private work separate from published content.
- Add organization briefings and aggregate activity reporting with clear visibility settings.
- Expand source coverage jurisdiction by jurisdiction. Each connector needs an owner, source documentation, fixtures, contract tests, health monitoring, and an accurate coverage label before launch.

**Completion criteria:** organization roles prevent unauthorized edits and private data disclosure; one organization completes a real coordination workflow; adding a jurisdiction does not require duplicating location definitions across the app.

## Technical approach and sequencing

- Keep React, Vite, Tailwind, and Firebase initially. Migrate touched code to TypeScript incrementally rather than rewriting the app.
- Introduce a shared data-access layer with validation, caching, cancellation, retries, and consistent error handling. Avoid repeating fetch logic across page components.
- Keep public civic facts independently versioned from private profiles, personal relevance, and organization work. Public static snapshots can remain useful for inexpensive browsing; private state belongs behind tested authorization.
- Use Firebase server functions or a small managed API for AI jobs and notifications. Choose after validating deployment access, budget, and operational ownership.
- Separate collection, normalization, summarization, and personalization so a profile change does not require re-scraping government websites.
- Add route-level lazy loading and review the Plotly payload after measuring the production bundle. Set performance budgets from a measured baseline and representative mobile conditions.
- Use staging, schema-compatible migrations, and feature flags. Pilot with one jurisdiction before widening rollout. Ensure rollback preserves saved actions and profiles.
- Upgrade dependencies deliberately after compatibility checks; framework version changes are supporting maintenance, not the primary product outcome.

Recommended first implementation slice: fix profile fallback and freshness semantics, establish the jurisdiction/data contracts, verify access rules, then ship one sourced issue card with a verified deadline and a private Save action. Complete the remaining foundation work before broad release or paid AI features.

## Validation and success measures

Establish baselines before setting numerical targets. Track privacy-conscious, aggregate measures without collecting political quiz answers in analytics.

- Activation: users who select a supported location and save a relevant action.
- Usefulness: users who return and complete a self-selected civic action; supplement with short interviews.
- Trust: source coverage, deadline accuracy, stale-record rate, and reported inaccuracies.
- Reliability: successful collection checks, recovery time, client errors, and notification delivery/duplication.
- Accessibility/performance: core journey audit results and mobile load/interaction measurements.
- Cost: AI cost per active user and per source update, with enforced limits.

Validate with a small resident pilot before expanding. Include interrupted requests, expired deadlines, canceled meetings, missing source fields, malformed AI responses, duplicate jobs, and unauthorized reads/writes in release checks.

## Scope decisions to confirm

1. Initial supported geography and the source quality required for that pilot.
2. Operating model: who owns source failures, corrections, and monthly AI/hosting costs.

Defer native mobile apps and broad geographic expansion until the core journey and data pipeline meet the completion criteria above. A responsive web experience serves the initial mobile need.

Estimate implementation milestones after pilot geography and deployment access are confirmed. The phases describe dependency order, not fixed calendar commitments.

## Implementation status — October 18, 2026

The resident-first upgrade is implemented locally. This does not mark every roadmap phase or production release criterion complete.

| Area | Implemented | Remaining |
| --- | --- | --- |
| Data trust | Shared registry and versioned contracts; legacy Orange County migration; validated atomic pipeline output; retries/date windows/pagination/deduplication; explicit failures/unsupported sources; source-local meeting times; archived analysis labels | Ongoing source-accuracy review, broader connector-specific outcome mapping, and review tooling |
| User isolation | Removed automatic fixed-profile fallback across dashboard/location/official views; account-scoped hooks and saved actions; private Firestore rules | Inspect existing deployed rules and migrate legacy organization membership documents in staging |
| Resident experience | Onboarding, briefing, public browsing, search/topic/timing filters, responsive navigation, source-first details, route recovery, keyboard focus and reduced-motion support | Resident pilot, full screen-reader/contrast audit, more decision/effort filters, richer changes briefing |
| Action workflow | Private save/plan/complete/dismiss, notes, undo while a card remains mounted, source-verified calendar export, editable local draft, export and deletion APIs | Persistent undo history, fuller followed-topic subscriptions, meaningful outcome/change notifications |
| AI | Authenticated callable service, bounded input/output/time, output validation, usage reservations, request deduplication; browser provider key storage removed | Configure secret and verify one paid call in staging; provider budget and operational ownership |
| Notifications | Verified email opt-in; scheduled verified-deadline digest/reminders; source-age/expiry suppression; delivery lease and provider idempotency; unsubscribe | Configure provider/sender/URL, verify real delivery, add larger-volume queueing and issue-change digests |
| Organizations | Private workspaces, invitations, roles, assigned actions/campaign labels/due dates, atomic activity records, allowlisted publication, removal/deletion controls | Organization pilot, richer campaign goals and aggregate reporting |
| Engineering | CI checks, lint, progressive contract/policy type checking, data/calendar/pipeline tests, Firestore permission tests, callable integration tests, browser journeys, lazy routes; heavyweight Plotly dependency replaced | Production monitoring dashboards, retention jobs, staged feature flags, measured performance goals |

See `docs/OPERATIONS.md` for deployment requirements and limitations. No production deployment, paid AI request, or email delivery has been performed.

### Verification evidence

- A live Austin collection succeeded after correcting the Legistar client to `austintexas`: 182 official matters and 5 official meeting records were collected. The 28 existing archived records were retained with their original provenance; no public-comment availability was invented.
- Meeting source records include the original official calendar URL, source-local time zone, exact start time where supplied, and verification timestamp. Five meetings were verified in the collected snapshot.
- The prior failed `austin` source returned HTTP 500. The shared registry now points to the working official client; source checks and pipeline failures remain explicit.
- Production build, lint, progressive type checks, data validation, unit/pipeline tests, permission tests, server integration tests, and browser journeys are exercised locally. Final counts are recorded in the release report below.

### Release verification report

The final local regression run passed:

- 12 JavaScript contract, calendar, AI-policy, and notification-policy tests.
- 8 Python pipeline tests covering failures, empty checks, malformed records, pagination, time zones, and exact status mappings.
- 3 Firestore emulator permission tests covering private profiles/actions, membership, role escalation, and server-controlled writes/publication.
- 3 callable integration tests covering invitations/roles/tasks/public fields, notification consent/unsubscribe, and account deletion.
- 7 Chromium browser journeys covering onboarding, saved notes/status persistence, account isolation, organization actions, public search/source browsing, 360px layout, route recovery, calendar download, and the explicit demo.
- ESLint, progressive TypeScript checks, data validation, production build, and `git diff --check`.

The previous ~4.76 MB Plotly-related JavaScript chunk has been removed. The remaining main client chunk is ~666 KB before compression (~176 KB gzip), so further measured performance work remains appropriate after the pilot. The default theme's secondary gray text and input boundaries were adjusted for clearer contrast.

Firebase emulators emitted metadata/auth-trigger warnings, but all asserted permission and callable/browser behaviors passed. No production Firebase rules or backend deployment was changed. No paid AI call or real email delivery was performed. Cloud credentials and provider secrets are not configured in this environment.
