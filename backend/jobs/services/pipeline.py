from datetime import datetime, timezone
from django.utils import timezone as dj_timezone
from ..models import Job, PipelineRun
from .filters import normalize_post
from .sources.reddit import RedditAPI

def run_pipeline(trigger="manual"):
    run = PipelineRun.objects.create(trigger=trigger)
    try:
        posts = RedditAPI().search_jobs()
        run.posts_seen = len(posts)
        for post in posts:
            normalized = normalize_post(post)
            if not normalized:
                continue
            timestamp = normalized.pop("posted_at", None)
            if timestamp:
                normalized["posted_at"] = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            _, created = Job.objects.update_or_create(
                source_post_id=normalized["source_post_id"],
                defaults=normalized,
            )
            if created:
                run.jobs_saved += 1
            else:
                run.duplicates_skipped += 1
        run.status = PipelineRun.Status.SUCCEEDED
    except Exception as exc:
        run.status = PipelineRun.Status.FAILED
        run.error_message = str(exc)[:4000]
    finally:
        run.finished_at = dj_timezone.now()
        run.save()
    return run
