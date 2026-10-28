from celery import shared_task
from .services.pipeline import run_pipeline

@shared_task
def run_pipeline_task(trigger="scheduled"):
    run = run_pipeline(trigger=trigger)
    return {"run_id": run.pk, "status": run.status, "jobs_saved": run.jobs_saved}
