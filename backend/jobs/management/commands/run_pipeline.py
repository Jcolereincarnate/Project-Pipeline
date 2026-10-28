from django.core.management.base import BaseCommand
from jobs.services.pipeline import run_pipeline

class Command(BaseCommand):
    help = "Run the Reddit job discovery pipeline once."

    def handle(self, *args, **options):
        run = run_pipeline(trigger="manual-cli")
        self.stdout.write(f"Run #{run.pk}: {run.status}; posts={run.posts_seen}; saved={run.jobs_saved}; duplicates={run.duplicates_skipped}")
        if run.error_message:
            self.stderr.write(run.error_message)
