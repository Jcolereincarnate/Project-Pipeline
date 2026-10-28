import re

ROLE_TERMS = [
    "backend engineer", "backend developer", "python developer", "django",
    "junior software engineer", "software engineer", "ai engineer", "machine learning",
    "full stack", "full-stack", "fullstack",
]
LOCATION_TERMS = ["remote", "worldwide", "anywhere", "nigeria", "lagos", "africa"]
EXPERIENCE_TERMS = ["junior", "mid-level", "mid level", "entry level", "1+ years", "2+ years", "3+ years"]

def normalize_post(post):
    title = (post.get("title") or "").strip()
    body = (post.get("selftext") or "").strip()
    text = f"{title}\n{body}".lower()
    tags = sorted({term for term in ROLE_TERMS if term in text})
    if not tags:
        return None

    location = next((term for term in LOCATION_TERMS if term in text), "")
    experience = next((term for term in EXPERIENCE_TERMS if term in text), "")
    remote = any(term in text for term in ["remote", "work from anywhere", "worldwide"])
    score = min(100, len(tags) * 25 + (20 if remote else 0) + (10 if experience else 0))

    return {
        "source_post_id": post["id"],
        "title": title[:500] or "Untitled job post",
        "description": body,
        "subreddit": post.get("subreddit", ""),
        "source_url": post.get("url") or f"https://www.reddit.com/comments/{post['id']}/",
        "posted_at": post.get("created_utc"),
        "location_label": location,
        "remote": remote,
        "experience_level": experience,
        "matched_tags": tags,
        "relevance_score": score,
    }
