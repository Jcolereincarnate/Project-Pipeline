from django.test import TestCase
from .services.filters import normalize_post

class NormalizePostTests(TestCase):
    def test_matches_backend_role(self):
        result = normalize_post({"id": "abc", "title": "Junior Python Django Backend Developer - Remote", "selftext": "2+ years", "subreddit": "PythonJobs", "url": "https://reddit.com/r/PythonJobs/comments/abc/"})
        self.assertIsNotNone(result)
        self.assertTrue(result["remote"])
        self.assertIn("django", result["matched_tags"])

    def test_ignores_unrelated_post(self):
        result = normalize_post({"id": "xyz", "title": "Looking for a graphic designer", "selftext": "", "subreddit": "jobs", "url": "https://reddit.com"})
        self.assertIsNone(result)
