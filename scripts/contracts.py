"""Versioned public civic data contract; keep aligned with shared/contracts.js."""
from urllib.parse import urlparse

SCHEMA_VERSION = 1

def validate_issue(issue):
    if not isinstance(issue, dict) or not isinstance(issue.get('id'), str) or not issue['id'] or not isinstance(issue.get('title'), str) or not issue['title']:
        raise ValueError('Issue needs an ID and title')
    if not isinstance(issue.get('summary'), str) or not isinstance(issue.get('policy_domains'), list) or any(not isinstance(d, str) for d in issue['policy_domains']):
        raise ValueError('Invalid issue summary or topics')
    if issue.get('source_url') is not None and urlparse(issue['source_url']).scheme not in ('https', 'http'):
        raise ValueError('Invalid source URL')
    if issue.get('schema_version', SCHEMA_VERSION) != SCHEMA_VERSION:
        raise ValueError('Unsupported issue version')
    return issue

def validate_collection(data):
    if not isinstance(data, dict) or not isinstance(data.get('issues'), list):
        raise ValueError('Invalid issue collection')
    if data.get('schema_version', SCHEMA_VERSION) != SCHEMA_VERSION:
        raise ValueError('Unsupported collection version')
    ids = set()
    for issue in data['issues']:
        validate_issue(issue)
        if issue['id'] in ids:
            raise ValueError('Duplicate issue ID')
        ids.add(issue['id'])
    return data
