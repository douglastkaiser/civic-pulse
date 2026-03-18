# Data Model — Civic Pulse

## Directory Structure

```
data/
├── profiles/        # User political profiles (manifesto, values, positions)
├── locations/       # Local government landscape per jurisdiction
├── issues/          # Civic issues with scoring and analysis
├── orgs/            # Organization data (mission, campaigns, strategy)
└── meta/            # Pipeline metadata (freshness, sync status)
```

## Future Auth Model

When this becomes a multi-user app with authentication:
- /data/profiles/ → database table: user_profiles (one per user, private)
- /data/locations/ → database table: locations (shared, one per jurisdiction)
- /data/issues/ → database table: issues (shared per location, scored per user)
- /data/orgs/ → database table: organizations (shared, with membership/roles)
- /data/meta/freshness.json → per-user + per-org job scheduling

## Privacy Model

- Profile data (manifesto, values, compass position): PRIVATE to user
- Location data (governing bodies, orgs, dynamics): SHARED across users in same jurisdiction
- Issue data (raw): SHARED. Issue scoring: PRIVATE (per-user).
- Organization data: PUBLIC (mission, campaigns) + PRIVATE (internal strategy, member list)
