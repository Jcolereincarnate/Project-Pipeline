from django.db import models

class PipelineRun(models.Model):
    class Status(models.TextChoices):
        RUNNING = "running", "Running"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.RUNNING)
    posts_seen = models.PositiveIntegerField(default=0)
    jobs_saved = models.PositiveIntegerField(default=0)
    duplicates_skipped = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    trigger = models.CharField(max_length=20, default="manual")

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"Run #{self.pk} ({self.status})"


class Job(models.Model):
    class Source(models.TextChoices):
        REDDIT = "reddit", "Reddit"

    class ApplicationStatus(models.TextChoices):
        NEW = "new", "New"
        SAVED = "saved", "Saved"
        INTERESTED = "interested", "Interested"
        APPLIED = "applied", "Applied"
        INTERVIEWING = "interviewing", "Interviewing"
        REJECTED = "rejected", "Rejected"
        OFFER = "offer", "Offer"

    source = models.CharField(max_length=20, choices=Source.choices, default=Source.REDDIT)
    source_post_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=500)
    company = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    subreddit = models.CharField(max_length=100, blank=True)
    source_url = models.URLField(max_length=1000)
    posted_at = models.DateTimeField(null=True, blank=True)
    location_label = models.CharField(max_length=250, blank=True)
    remote = models.BooleanField(default=False)
    experience_level = models.CharField(max_length=50, blank=True)
    matched_tags = models.JSONField(default=list, blank=True)
    relevance_score = models.PositiveSmallIntegerField(default=0)
    application_status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.NEW)
    notes = models.TextField(blank=True)
    discovered_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-posted_at", "-discovered_at"]

    def __str__(self):
        return self.title
