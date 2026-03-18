# Civic Pulse

Political intelligence dashboard for local civic engagement.

## What is this?

Civic Pulse monitors local government activity, maps it against your political priorities, and tells you what to do about it. It's the local political infrastructure that should exist but doesn't.

## Architecture

- Static React app hosted on GitHub Pages
- Data stored as JSON files in /data/
- Data pipeline (Python + Anthropic API) runs via GitHub Actions
- Frontend reads data files at build time

## For Developers

- `npm install` → `npm run dev` for local development
- `npm run build` to build for production
- Push to main to trigger GitHub Pages deployment
- Data pipeline: `python scripts/pipeline.py` (requires ANTHROPIC_API_KEY)

## Data Freshness

The app tracks when each data layer was last updated and displays staleness warnings. Trigger a data refresh via GitHub Actions (manual dispatch) or wait for the weekly cron.

## Future Roadmap

- [ ] User authentication and private profiles
- [ ] Automated scraping pipeline (Legistar API + generic scrapers)
- [ ] Email digest generation
- [ ] Multi-user organization management
- [ ] Public organization pages
- [ ] Mobile app
