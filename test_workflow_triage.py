import unittest
from workflow_triage import scan


class TriageTests(unittest.TestCase):
    def rules(self, text):
        return [item['rule'] for item in scan(text)]

    def test_mutable_action(self):
        self.assertEqual(self.rules('permissions: {}\n- uses: actions/checkout@v4'), ['MUTABLE_ACTION'])

    def test_sha_and_local_actions(self):
        text = 'permissions: {}\n- uses: owner/action@' + 'a' * 40 + '\n- uses: ./.github/actions/local'
        self.assertEqual(self.rules(text), [])

    def test_missing_permissions_is_review_only(self):
        self.assertEqual(self.rules('name: Example'), ['PERMISSIONS_REVIEW'])

    def test_broad_permissions(self):
        self.assertEqual(self.rules('permissions: write-all'), ['WRITE_ALL'])

    def test_target_trigger(self):
        self.assertEqual(self.rules('permissions: {}\non: [pull_request_target]'), ['TARGET_TRIGGER_REVIEW'])

    def test_event_expression(self):
        self.assertEqual(self.rules('permissions: {}\nrun: echo "${{ github.event.issue.title }}"'), ['EVENT_INPUT_REVIEW'])

    def test_comments_ignored(self):
        self.assertEqual(self.rules('permissions: {}\n# - uses: owner/action@v1'), [])

    def test_container_digest(self):
        self.assertEqual(self.rules('permissions: {}\n- uses: docker://alpine@sha256:' + 'a' * 64), [])
        self.assertEqual(self.rules('permissions: {}\n- uses: docker://alpine:latest'), ['MUTABLE_IMAGE'])

    def test_line_numbers(self):
        findings = scan('permissions: {}\n\n- uses: owner/action@v1', 'sample.yml')
        self.assertEqual(findings[0]['line'], 3)
        self.assertEqual(findings[0]['file'], 'sample.yml')


if __name__ == '__main__':
    unittest.main()
