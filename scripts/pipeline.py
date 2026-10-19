"""Collect source facts separately from private user profiles. No AI is needed to publish source records."""
import argparse
import json
import logging
import os
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from contracts import SCHEMA_VERSION, validate_collection

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    requests = None

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / 'public' / 'data'
REGISTRY = json.loads((ROOT / 'shared' / 'jurisdictions.json').read_text())['jurisdictions']
log = logging.getLogger('civic-pulse')


def now():
    return datetime.now(timezone.utc).isoformat()


def load_json(path):
    return json.loads(path.read_text()) if path.exists() else None


def save_json(path, data):
    """Publish a complete validated file atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def update_freshness(location_id, **fields):
    path = DATA_DIR / 'meta' / 'freshness.json'
    data = load_json(path) or {}
    data['schema_version'] = SCHEMA_VERSION
    data.setdefault('locations', {}).setdefault(location_id, {}).update(fields)
    save_json(path, data)


class LegistarScraper:
    def __init__(self, base_url, session=None):
        if session is None:
            if requests is None:
                raise RuntimeError('requests is required to collect source data')
            session = requests.Session()
            retry = Retry(total=2, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=['GET'], respect_retry_after_header=False)
            session.mount('https://', HTTPAdapter(max_retries=retry))
        self.session = session
        self.base_url = base_url.rstrip('/')

    def pages(self, resource, params):
        records = {}
        for page in range(100):
            response = self.session.get(f'{self.base_url}/{resource}', params={**params, '$top': 100, '$skip': page * 100}, timeout=(10, 30))
            response.raise_for_status()
            batch = response.json()
            if not isinstance(batch, list):
                raise ValueError('Source response must be a list')
            key = 'MatterId' if resource == 'matters' else 'EventId'
            for item in batch:
                if not isinstance(item, dict) or key not in item:
                    raise ValueError('Source record missing stable ID')
                records[item[key]] = item
            if len(batch) < 100:
                return list(records.values())
        raise RuntimeError('Pagination limit reached; refusing to publish partial collection')

    def fetch_recent_matters(self, days_back=30):
        since = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime('%Y-%m-%dT%H:%M:%S')
        return self.pages('matters', {'$filter': f"MatterLastModifiedUtc ge datetime'{since}'", '$orderby': 'MatterLastModifiedUtc asc,MatterId asc'})

    def fetch_events(self, days_ahead=60):
        # Query broadly in UTC; source-local timestamps remain unverified until reconciled.
        start = (datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%dT00:00:00')
        end = (datetime.now(timezone.utc) + timedelta(days=days_ahead)).strftime('%Y-%m-%dT23:59:59')
        return self.pages('events', {'$filter': f"EventDate ge datetime'{start}' and EventDate le datetime'{end}'", '$orderby': 'EventDate asc,EventId asc'})


def source_topics(title):
    """Navigation hints from simple keywords; these are not source-verified policy positions."""
    title = title.lower()
    keywords = {
        'Housing': ['housing', 'affordable', 'residential'],
        'Transportation': ['transportation', 'transit', 'street', 'sidewalk', 'mobility'],
        'Education': ['school', 'education'],
        'Public Safety': ['police', 'fire department', 'public safety', 'emergency'],
        'Environment': ['climate', 'environment', 'water', 'flood', 'park'],
        'Budget': ['budget', 'tax', 'funding', 'contract'],
        'Land Use': ['zoning', 'rezon', 'land use'],
        'Healthcare': ['health', 'medical'],
    }
    return [topic for topic, terms in keywords.items() if any(term in title for term in terms)]


def normalize_matter(raw, jurisdiction, fetched_at):
    if not raw.get('MatterTitle') or raw.get('MatterId') is None:
        raise ValueError('Matter lacks title or stable ID')
    # Only exact, reviewed source statuses become outcomes; never infer from a title.
    statuses = {'passed': 'passed', 'adopted': 'passed', 'failed': 'rejected', 'rejected': 'rejected', 'postponed': 'postponed', 'withdrawn': 'canceled', 'agenda ready': 'upcoming'}
    source_status = raw.get('MatterStatusName') or ''
    return {
        'schema_version': SCHEMA_VERSION,
        'id': f"legistar-{jurisdiction['id']}-{raw['MatterId']}",
        'external_id': str(raw['MatterId']),
        'title': raw['MatterTitle'][:180] + ('…' if len(raw['MatterTitle']) > 180 else ''),
        'summary': raw['MatterTitle'],
        'governing_body': raw.get('MatterBodyName') or 'See source record',
        'policy_domains': source_topics(raw['MatterTitle']),
        'topic_method': 'keyword_navigation_hint',
        'status': statuses.get(source_status.lower(), 'unresolved'),
        'source_status': source_status,
        'source_url': raw.get('MatterWebLink') or f"{jurisdiction['source']['base_url']}/matters/{raw['MatterId']}",
        'source_updated_at': raw.get('MatterLastModifiedUtc'),
        'fetched_at': fetched_at,
        'timezone': jurisdiction['timezone'],
        'provenance': 'source_record',
        'meeting_date': (raw.get('MatterAgendaDate') or '').split('T')[0] or None,
        'public_comment': {'available': False, 'verified': False, 'deadline': None, 'instructions': 'Check the official record for current participation instructions.'},
    }


def normalize_event(raw, jurisdiction, fetched_at):
    from zoneinfo import ZoneInfo
    if not raw.get('EventId') or not raw.get('EventBodyName'):
        raise ValueError('Meeting lacks ID or governing body')
    url = raw.get('EventInSiteURL') or raw.get('EventAgendaFile')
    date = (raw.get('EventDate') or '').split('T')[0]
    starts_at = None
    try:
        local = datetime.strptime(f"{date} {raw.get('EventTime', '')}", '%Y-%m-%d %I:%M %p')
        # Ambiguous and nonexistent wall-clock times need manual confirmation.
        zone = ZoneInfo(jurisdiction['timezone'])
        local = local.replace(tzinfo=zone)
        if local.replace(fold=0).utcoffset() == local.replace(fold=1).utcoffset():
            starts_at = local.isoformat()
    except (ValueError, TypeError):
        pass
    canceled = 'cancel' in str(raw.get('EventAgendaStatusName', '')).lower()
    return {
        'schema_version': SCHEMA_VERSION,
        'id': f"legistar-event-{jurisdiction['id']}-{raw['EventId']}",
        'external_id': str(raw['EventId']),
        'title': f"{raw['EventBodyName']} meeting",
        'summary': raw.get('EventComment') or f"Official calendar entry for {raw['EventBodyName']}. Review the agenda before attending.",
        'governing_body': raw['EventBodyName'],
        'policy_domains': source_topics(raw['EventBodyName']),
        'topic_method': 'keyword_navigation_hint',
        'status': 'canceled' if canceled else 'upcoming',
        'source_url': url,
        'meeting_date': date or None,
        'timezone': jurisdiction['timezone'],
        'fetched_at': fetched_at,
        'provenance': 'source_record',
        'meeting': {'starts_at': starts_at, 'timezone': jurisdiction['timezone'], 'source_url': url, 'verified': bool(starts_at and url and not canceled), 'verified_at': fetched_at},
        'public_comment': {'available': False, 'verified': False, 'deadline': None, 'instructions': 'See the official agenda for participation rules.'},
    }


def run_location(jurisdiction, scrape_only=False):
    location_id = jurisdiction['id']
    update_freshness(location_id, last_attempt_at=now())
    source = jurisdiction.get('source')
    if not source or source['type'] != 'legistar':
        update_freshness(location_id, status='unsupported', needs_rescrape=True, error='Automated source is not configured.')
        return 'unsupported'
    try:
        scraper = LegistarScraper(source['base_url'])
        raw = scraper.fetch_recent_matters()
        events = scraper.fetch_events()
        fetched_at = now()
        issues = [normalize_matter(item, jurisdiction, fetched_at) for item in raw] + [normalize_event(item, jurisdiction, fetched_at) for item in events]
        data = validate_collection({'schema_version': SCHEMA_VERSION, 'last_successful_fetch_at': fetched_at, 'issues': issues})
        previous = load_json(DATA_DIR / 'issues' / f'{location_id}.json') or {}
        previous_records = {i['id']: ({**i, 'provenance': i.get('provenance', 'legacy_snapshot'), 'snapshot_at': i.get('snapshot_at') or previous.get('last_scraped')} if i.get('provenance') != 'source_record' else i) for i in previous.get('issues', [])}
        def fingerprint(item):
            result = {k: v for k, v in item.items() if k != 'fetched_at'}
            if isinstance(result.get('meeting'), dict):
                result['meeting'] = {k: v for k, v in result['meeting'].items() if k != 'verified_at'}
            return result
        changed = any(fingerprint(previous_records.get(i['id'], {})) != fingerprint(i) for i in issues)
        save_json(DATA_DIR / 'sources' / f'{location_id}.json', {'schema_version': SCHEMA_VERSION, 'fetched_at': fetched_at, 'matters': raw, 'events': events, 'timezone': jurisdiction['timezone']})
        if not scrape_only:
            # This is a rolling source window. Retain older records for followed issues and outcomes,
            # but keep their own fetched_at so an unchanged old record never looks newly checked.
            if issues:
                for issue in issues:
                    previous_records[issue['id']] = issue
                data['issues'] = list(previous_records.values())
                validate_collection(data)
                save_json(DATA_DIR / 'issues' / f'{location_id}.json', data)
            elif not previous:
                save_json(DATA_DIR / 'issues' / f'{location_id}.json', data)
        update_freshness(location_id, status='updated' if changed and not scrape_only else 'no_changes', last_successful_fetch_at=fetched_at, needs_rescrape=False, error=None, record_count=len(issues))
        return 'success'
    except Exception as error:
        log.error('Collection failed for %s: %s', location_id, type(error).__name__)
        update_freshness(location_id, status='failed', needs_rescrape=True, error='Source collection failed; last known good records retained.')
        return 'failed'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('locations', nargs='*')
    parser.add_argument('--scrape-only', action='store_true')
    args = parser.parse_args()
    ids = {j['id'] for j in REGISTRY}
    if any(location_id not in ids for location_id in args.locations):
        parser.error('Unknown location; choose a jurisdiction from shared/jurisdictions.json')
    selected = [j for j in REGISTRY if not args.locations or j['id'] in args.locations]
    results = [run_location(j, args.scrape_only) for j in selected]
    path = DATA_DIR / 'meta' / 'freshness.json'
    data = load_json(path) or {}
    data.update(last_full_run=now(), last_run_status='error' if 'failed' in results else 'partial' if 'unsupported' in results else 'success')
    save_json(path, data)
    return 1 if 'failed' in results else 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    raise SystemExit(main())
