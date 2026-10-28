from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="PipelineRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(choices=[("running", "Running"), ("succeeded", "Succeeded"), ("failed", "Failed")], default="running", max_length=12)),
                ("posts_seen", models.PositiveIntegerField(default=0)),
                ("jobs_saved", models.PositiveIntegerField(default=0)),
                ("duplicates_skipped", models.PositiveIntegerField(default=0)),
                ("error_message", models.TextField(blank=True)),
                ("trigger", models.CharField(default="manual", max_length=20)),
            ],
            options={"ordering": ["-started_at"]},
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source", models.CharField(choices=[("reddit", "Reddit")], default="reddit", max_length=20)),
                ("source_post_id", models.CharField(max_length=100, unique=True)),
                ("title", models.CharField(max_length=500)),
                ("company", models.CharField(blank=True, max_length=250)),
                ("description", models.TextField(blank=True)),
                ("subreddit", models.CharField(blank=True, max_length=100)),
                ("source_url", models.URLField(max_length=1000)),
                ("posted_at", models.DateTimeField(blank=True, null=True)),
                ("location_label", models.CharField(blank=True, max_length=250)),
                ("remote", models.BooleanField(default=False)),
                ("experience_level", models.CharField(blank=True, max_length=50)),
                ("matched_tags", models.JSONField(blank=True, default=list)),
                ("relevance_score", models.PositiveSmallIntegerField(default=0)),
                ("application_status", models.CharField(choices=[("new", "New"), ("saved", "Saved"), ("interested", "Interested"), ("applied", "Applied"), ("interviewing", "Interviewing"), ("rejected", "Rejected"), ("offer", "Offer")], default="new", max_length=20)),
                ("notes", models.TextField(blank=True)),
                ("discovered_at", models.DateTimeField(auto_now_add=True)),
                ("last_seen_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-posted_at", "-discovered_at"]},
        ),
    ]
