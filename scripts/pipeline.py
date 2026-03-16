"""
Civic Pulse data pipeline.

Scrapes local government data sources (Legistar, custom scrapers),
processes with Claude API, and outputs structured JSON for the dashboard.

Model: claude-haiku-4-5-20251001

Usage:
    python scripts/pipeline.py                  # Run all profiles
    python scripts/pipeline.py austin-78702     # Run single profile
    python scripts/pipeline.py --scrape-only    # Scrape without AI processing
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import requests
except ImportError:
    requests = None

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "claude-haiku-4-5-20251001"
DATA_DIR = Path(__file__).resolve().parent.parent / "public" / "data"
PROFILES_DIR = DATA_DIR / "profiles"
LOCATIONS_DIR = DATA_DIR / "locations"
ISSUES_DIR = DATA_DIR / "issues"
META_DIR = DATA_DIR / "meta"

PROFILE_IDS = [
    "austin-78702",
    "brooklyn-ny",
    "madison-wi",
    "cambridge-ma",
    "brookline-ma",
]

# Legistar-based jurisdictions and their API base URLs
LEGISTAR_SOURCES = {
    "austin-78702": {
        "client": "austin",
        "base_url": "https://webapi.legistar.com/v1/austin",
        "body_names": ["Austin City Council"],
    },
    "madison-wi": {
        "client": "madison",
        "base_url": "https://webapi.legistar.com/v1/madison",
        "body_names": ["Madison Common Council"],
    },
}

# Non-Legistar sources (placeholder for custom scrapers)
CUSTOM_SOURCES = {
    "brooklyn-ny": {
        "type": "nyc_legistar",
        "base_url": "https://legistar.council.nyc.gov/",
    },
    "cambridge-ma": {
        "type": "civic_clerk",
        "note": "Cambridge uses its own agenda system",
    },
    "brookline-ma": {
        "type": "town_meeting",
        "note": "Brookline Town Meeting — manual or custom scraper needed",
    },
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("civic-pulse")


# ---------------------------------------------------------------------------
# Legistar Scraper
# ---------------------------------------------------------------------------


class LegistarScraper:
    """Fetches recent legislation from Legistar Web API."""

    def __init__(self, client: str, base_url: str, body_names: list[str]):
        self.client = client
        self.base_url = base_url.rstrip("/")
        self.body_names = body_names

    def fetch_recent_matters(self, days_back: int = 30) -> list[dict]:
        """Fetch matters (legislation items) from the last N days."""
        if requests is None:
            log.warning("requests not installed — skipping Legistar scrape for %s", self.client)
            return []

        from_date = datetime.now(timezone.utc).isoformat()
        url = f"{self.base_url}/matters"
        params = {
            "$orderby": "MatterLastModifiedUtc desc",
            "$top": 50,
        }

        try:
            log.info("Fetching matters from Legistar (%s)...", self.client)
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            matters = resp.json()
            log.info("Fetched %d matters from %s", len(matters), self.client)
            return matters
        except Exception as e:
            log.error("Legistar fetch failed for %s: %s", self.client, e)
            return []

    def fetch_events(self, days_ahead: int = 60) -> list[dict]:
        """Fetch upcoming calendar events (meetings)."""
        if requests is None:
            return []

        url = f"{self.base_url}/events"
        params = {
            "$orderby": "EventDate desc",
            "$top": 20,
        }

        try:
            log.info("Fetching events from Legistar (%s)...", self.client)
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            events = resp.json()
            log.info("Fetched %d events from %s", len(events), self.client)
            return events
        except Exception as e:
            log.error("Legistar events fetch failed for %s: %s", self.client, e)
            return []


class GenericScraper:
    """Placeholder for non-Legistar jurisdictions."""

    def __init__(self, profile_id: str, config: dict):
        self.profile_id = profile_id
        self.config = config

    def fetch(self) -> list[dict]:
        log.warning(
            "No scraper implemented for %s (type: %s). Skipping.",
            self.profile_id,
            self.config.get("type", "unknown"),
        )
        return []


# ---------------------------------------------------------------------------
# Claude API Processing
# ---------------------------------------------------------------------------


def score_issues(
    profile: dict, location: dict, raw_matters: list[dict]
) -> list[dict]:
    """
    Use Claude to analyze raw scraped data and produce scored issues.

    Takes the user's profile (values, salience, manifesto) and raw legislative
    data, returns structured issues with importance/impact scores, quadrant
    assignments, and personalized analysis.
    """
    if anthropic is None:
        log.error("anthropic package not installed — cannot score issues")
        return []

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set — cannot score issues")
        return []

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = """You are a political intelligence analyst for Civic Pulse, a local government monitoring tool.
Your job is to analyze raw legislative data and score each item's relevance to a specific person based on their political profile.

For each issue, produce:
- id: short kebab-case identifier
- title: concise title
- governing_body: which body is considering this
- governing_body_type: type of body
- meeting_date: ISO date or null
- summary: 2-3 sentence summary
- policy_domains: array of relevant domains
- decision_type: vote/discussion/election/petition
- geographic_scope: neighborhood/district/citywide/countywide
- public_comment: { available: bool, deadline: string|null, instructions: string }
- estimated_contestedness: low/medium/high
- importance_score: 0-100 (how much this matters to THIS person based on their values and salience)
- impact_score: 0-100 (how much impact this person could have on the outcome)
- quadrant: act_now (high importance + high impact), know (low importance + high impact), watch (high importance + low impact), or background (low both)
- why_it_matters_to_you: 1-2 sentences explaining personal relevance
- source_url: original source if available

Return a JSON array of issue objects. Be practical and politically realistic."""

    user_content = f"""Profile:
{json.dumps(profile, indent=2)}

Location context:
{json.dumps(location, indent=2)}

Raw legislative data to analyze:
{json.dumps(raw_matters[:20], indent=2)}

Analyze these items and return a scored JSON array of issues."""

    try:
        log.info("Calling Claude API to score %d items...", len(raw_matters[:20]))
        message = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )

        response_text = message.content[0].text

        # Extract JSON from response (handle markdown code blocks)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        issues = json.loads(response_text)
        log.info("Claude returned %d scored issues", len(issues))
        return issues

    except Exception as e:
        log.error("Claude API call failed: %s", e)
        return []


def generate_next_steps(profile: dict, location: dict, issues: list[dict]) -> dict:
    """
    Use Claude to generate personalized next steps based on scored issues.

    Returns a dict with sections: immediate, this_month, medium_term, strategic.
    """
    if anthropic is None or not os.environ.get("ANTHROPIC_API_KEY"):
        log.warning("Cannot generate next steps — API not available")
        return None

    client = anthropic.Anthropic()

    system_prompt = """You are a practical political advisor. Given a person's profile, their local political landscape, and scored issues, generate concrete next steps.

Return JSON with these sections:
- immediate: actions for this week (array of {action, detail, time, impact, reason})
- this_month: actions for this month
- medium_term: actions for the next 90 days
- strategic: longer-term opportunities

Each action should be specific, actionable, and realistic given the person's engagement_appetite.
Impact levels: HIGH, VERY HIGH, MEDIUM, LOW EFFORT ONGOING VALUE.
Time estimates should be realistic."""

    user_content = f"""Profile:
{json.dumps(profile, indent=2)}

Location:
{json.dumps(location, indent=2)}

Scored issues:
{json.dumps(issues, indent=2)}

Generate personalized next steps."""

    try:
        log.info("Generating next steps via Claude API...")
        message = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )

        response_text = message.content[0].text
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        steps = json.loads(response_text)
        log.info("Generated next steps with %d sections", len(steps))
        return steps

    except Exception as e:
        log.error("Next steps generation failed: %s", e)
        return None


# ---------------------------------------------------------------------------
# Data I/O
# ---------------------------------------------------------------------------


def load_json(path: Path) -> dict | list | None:
    """Load a JSON file, returning None if it doesn't exist."""
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def save_json(path: Path, data: dict | list) -> None:
    """Save data as formatted JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    log.info("Saved %s", path)


def update_freshness(profile_id: str, **fields) -> None:
    """Update freshness.json for a given profile."""
    freshness_path = META_DIR / "freshness.json"
    freshness = load_json(freshness_path) or {"profiles": {}}

    if profile_id not in freshness["profiles"]:
        freshness["profiles"][profile_id] = {}

    now = datetime.now(timezone.utc).isoformat()
    for key, value in fields.items():
        freshness["profiles"][profile_id][key] = value if value is not True else now

    freshness["last_full_run"] = now
    save_json(freshness_path, freshness)


# ---------------------------------------------------------------------------
# Pipeline Orchestration
# ---------------------------------------------------------------------------


def run_scrape(profile_id: str) -> list[dict]:
    """Scrape raw data for a profile using the appropriate scraper."""
    if profile_id in LEGISTAR_SOURCES:
        cfg = LEGISTAR_SOURCES[profile_id]
        scraper = LegistarScraper(
            client=cfg["client"],
            base_url=cfg["base_url"],
            body_names=cfg["body_names"],
        )
        return scraper.fetch_recent_matters()
    elif profile_id in CUSTOM_SOURCES:
        scraper = GenericScraper(profile_id, CUSTOM_SOURCES[profile_id])
        return scraper.fetch()
    else:
        log.warning("No scraper configured for %s", profile_id)
        return []


def run_profile(profile_id: str, scrape_only: bool = False) -> None:
    """Run the full pipeline for a single profile."""
    log.info("=" * 60)
    log.info("Processing profile: %s", profile_id)
    log.info("=" * 60)

    # Load existing data
    profile = load_json(PROFILES_DIR / f"{profile_id}.json")
    location = load_json(LOCATIONS_DIR / f"{profile_id}.json")

    if not profile:
        log.error("No profile found for %s — skipping", profile_id)
        return

    # Step 1: Scrape
    raw_data = run_scrape(profile_id)
    update_freshness(profile_id, location_scraped=True)

    if scrape_only:
        log.info("Scrape-only mode — skipping AI processing")
        if raw_data:
            # Save raw data for inspection
            save_json(ISSUES_DIR / f"{profile_id}-raw.json", raw_data)
        return

    if not raw_data:
        log.warning("No data scraped for %s — preserving existing issues", profile_id)
        update_freshness(profile_id, issues_scraped=True, needs_rescrape=True)
        return

    # Step 2: Score issues with Claude
    issues = score_issues(profile, location, raw_data)
    if issues:
        issues_data = {
            "last_scraped": datetime.now(timezone.utc).isoformat(),
            "issues": issues,
        }
        save_json(ISSUES_DIR / f"{profile_id}.json", issues_data)
        update_freshness(
            profile_id,
            issues_scraped=True,
            issues_scored=True,
            needs_rescrape=False,
        )
    else:
        log.warning("No issues produced for %s", profile_id)

    # Step 3: Generate next steps
    if issues and profile.get("manifesto_inputs_complete"):
        steps = generate_next_steps(profile, location, issues)
        if steps:
            profile["next_steps"] = steps
            save_json(PROFILES_DIR / f"{profile_id}.json", profile)
            update_freshness(profile_id, next_steps_generated=True)

    log.info("Completed %s", profile_id)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Civic Pulse data pipeline — scrape and process political data"
    )
    parser.add_argument(
        "profiles",
        nargs="*",
        default=PROFILE_IDS,
        help="Profile IDs to process (default: all)",
    )
    parser.add_argument(
        "--scrape-only",
        action="store_true",
        help="Only scrape data, skip Claude API processing",
    )
    args = parser.parse_args()

    # Validate profile IDs
    for pid in args.profiles:
        if pid not in PROFILE_IDS:
            log.error("Unknown profile: %s (valid: %s)", pid, ", ".join(PROFILE_IDS))
            sys.exit(1)

    log.info("Civic Pulse pipeline starting")
    log.info("Profiles: %s", ", ".join(args.profiles))
    log.info("Mode: %s", "scrape-only" if args.scrape_only else "full pipeline")

    errors = []
    for pid in args.profiles:
        try:
            run_profile(pid, scrape_only=args.scrape_only)
        except Exception as e:
            log.error("Pipeline failed for %s: %s", pid, e)
            errors.append(f"{pid}: {e}")

    # Update overall run status
    freshness_path = META_DIR / "freshness.json"
    freshness = load_json(freshness_path) or {}
    freshness["last_full_run"] = datetime.now(timezone.utc).isoformat()
    freshness["last_run_status"] = "error" if errors else "success"
    freshness["last_run_errors"] = errors
    save_json(freshness_path, freshness)

    if errors:
        log.error("Pipeline completed with %d errors", len(errors))
        sys.exit(1)
    else:
        log.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()
