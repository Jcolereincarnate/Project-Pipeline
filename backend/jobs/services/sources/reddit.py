import time
import requests
from django.conf import settings

class RedditAccessNotConfigured(RuntimeError):
    pass

class RedditAPI:
    TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
    API_BASE = "https://oauth.reddit.com"

    def __init__(self):
        if not settings.REDDIT_ENABLED:
            raise RedditAccessNotConfigured(
                "Reddit collection is disabled. Confirm Data API access approval, configure OAuth credentials, "
                "and set REDDIT_ENABLED=True in your environment."
            )
        if not settings.REDDIT_CLIENT_ID or not settings.REDDIT_CLIENT_SECRET:
            raise RedditAccessNotConfigured("Reddit OAuth client ID/secret are missing.")

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": settings.REDDIT_USER_AGENT})
        response = self.session.post(
            self.TOKEN_URL,
            auth=(settings.REDDIT_CLIENT_ID, settings.REDDIT_CLIENT_SECRET),
            data={"grant_type": "client_credentials"},
            timeout=20,
        )
        response.raise_for_status()
        self.session.headers["Authorization"] = f"bearer {response.json()['access_token']}"

    def search_subreddit(self, subreddit, query, limit=50):
        response = self.session.get(
            f"{self.API_BASE}/r/{subreddit}/search",
            params={"q": query, "sort": "new", "t": "month", "limit": min(limit, 100), "restrict_sr": "true"},
            timeout=20,
        )
        response.raise_for_status()
        return [item["data"] for item in response.json().get("data", {}).get("children", [])]

    def search_jobs(self):
        # Keep requests bounded. Adjust terms and subreddits after validating API access.
        queries = [
            '"backend engineer" OR "backend developer"',
            '"Python developer" OR Django',
            '"junior software engineer"',
            '"AI engineer" OR "machine learning engineer"',
            '"full stack developer" OR "full-stack developer"',
        ]
        seen = {}
        for subreddit in settings.REDDIT_SUBREDDITS:
            for query in queries:
                for post in self.search_subreddit(subreddit, query, settings.REDDIT_SEARCH_LIMIT):
                    seen[post["id"]] = post
                time.sleep(1)  # conservative pacing; still obey current Reddit limits/policies
        return list(seen.values())
