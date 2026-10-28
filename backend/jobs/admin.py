from django.contrib import admin
from .models import Job, PipelineRun

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "subreddit", "posted_at", "application_status", "relevance_score")
    list_filter = ("application_status", "remote", "subreddit")
    search_fields = ("title", "company", "description", "source_post_id")

@admin.register(PipelineRun)
class PipelineRunAdmin(admin.ModelAdmin):
    list_display = ("id", "started_at", "finished_at", "status", "posts_seen", "jobs_saved")
    list_filter = ("status", "trigger")
