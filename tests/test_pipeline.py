import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import pipeline

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.patch = patch.object(pipeline, 'DATA_DIR', Path(self.temp.name)); self.patch.start()
        self.jurisdiction = pipeline.REGISTRY[0]
        self.issue_path = pipeline.DATA_DIR / 'issues' / f"{self.jurisdiction['id']}.json"
        self.original = {'issues': [{'id': 'old', 'title': 'Old record', 'summary': 'Keep me', 'policy_domains': []}]}
        pipeline.save_json(self.issue_path, self.original)
    def tearDown(self):
        self.patch.stop(); self.temp.cleanup()
    def status(self):
        return json.loads((pipeline.DATA_DIR / 'meta' / 'freshness.json').read_text())['locations'][self.jurisdiction['id']]
    def test_failure_retains_data_and_does_not_advance_success(self):
        pipeline.update_freshness(self.jurisdiction['id'], last_successful_fetch_at='2026-01-01T00:00:00Z')
        with patch.object(pipeline, 'LegistarScraper', side_effect=RuntimeError('offline')):
            self.assertEqual(pipeline.run_location(self.jurisdiction), 'failed')
        self.assertEqual(json.loads(self.issue_path.read_text()), self.original)
        self.assertEqual(self.status()['last_successful_fetch_at'], '2026-01-01T00:00:00Z')
        self.assertIs(self.status()['needs_rescrape'], True)
    def test_empty_success_is_not_a_failure_or_fresh_rewrite(self):
        with patch.object(pipeline, 'LegistarScraper') as cls:
            cls.return_value.fetch_recent_matters.return_value = []
            cls.return_value.fetch_events.return_value = []
            self.assertEqual(pipeline.run_location(self.jurisdiction), 'success')
        self.assertEqual(self.status()['status'], 'no_changes')
        self.assertIs(self.status()['needs_rescrape'], False)
        self.assertEqual(json.loads(self.issue_path.read_text()), self.original)
    def test_invalid_source_does_not_replace_valid_data(self):
        with patch.object(pipeline, 'LegistarScraper') as cls:
            cls.return_value.fetch_recent_matters.return_value = [{'MatterId': 1}]
            cls.return_value.fetch_events.return_value = []
            self.assertEqual(pipeline.run_location(self.jurisdiction), 'failed')
        self.assertEqual(json.loads(self.issue_path.read_text()), self.original)
    def test_unsupported_source_is_explicit(self):
        unsupported = {**self.jurisdiction, 'source': None}
        self.assertEqual(pipeline.run_location(unsupported), 'unsupported')
        self.assertNotIn('last_successful_fetch_at', self.status())
    def test_pagination_filters_and_deduplication(self):
        session = Mock()
        page1 = [{'MatterId': i} for i in range(100)]
        page2 = [{'MatterId': 99}, {'MatterId': 100}]
        responses = [Mock(), Mock()]
        for response, batch in zip(responses, [page1, page2]): response.json.return_value = batch
        session.get.side_effect = responses
        result = pipeline.LegistarScraper('https://example.gov', session).fetch_recent_matters(7)
        self.assertEqual(len(result), 101)
        self.assertIn('$filter', session.get.call_args_list[0].kwargs['params'])
        self.assertEqual(session.get.call_args_list[1].kwargs['params']['$skip'], 100)
    def test_source_normalization_does_not_invent_deadlines(self):
        normalized = pipeline.normalize_matter({'MatterId': 4, 'MatterTitle': 'A title', 'MatterWebLink': 'https://example.gov'}, self.jurisdiction, pipeline.now())
        self.assertEqual(normalized['external_id'], '4')
        self.assertFalse(normalized['public_comment']['verified'])
        self.assertIsNone(normalized['meeting_date'])

    def test_meeting_timezone_and_unverified_ambiguous_time(self):
        raw = {'EventId': 1, 'EventBodyName': 'City Council', 'EventDate': '2026-10-22T00:00:00', 'EventTime': '10:00 AM', 'EventInSiteURL': 'https://example.gov/agenda'}
        normalized = pipeline.normalize_event(raw, self.jurisdiction, pipeline.now())
        self.assertTrue(normalized['meeting']['verified'])
        self.assertEqual(normalized['meeting']['starts_at'], '2026-10-22T10:00:00-05:00')
        self.assertFalse(normalized['public_comment']['available'])
        ambiguous = pipeline.normalize_event({**raw, 'EventDate': '2026-11-01T00:00:00', 'EventTime': '1:30 AM'}, self.jurisdiction, pipeline.now())
        self.assertFalse(ambiguous['meeting']['verified'])
    def test_reviewed_status_mapping_and_source_links(self):
        raw = {'MatterId': 4, 'MatterTitle': 'Housing budget decision', 'MatterStatusName': 'Passed'}
        record = pipeline.normalize_matter(raw, self.jurisdiction, pipeline.now())
        self.assertEqual(record['status'], 'passed')
        self.assertIn('Housing', record['policy_domains'])
        self.assertTrue(record['source_url'].endswith('/matters/4'))
        unknown = pipeline.normalize_matter({**raw, 'MatterStatusName': 'Unknown custom status'}, self.jurisdiction, pipeline.now())
        self.assertEqual(unknown['status'], 'unresolved')

if __name__ == '__main__': unittest.main()
