from django.urls import path
from .views import JobListView, PipelineRunListView, trigger_pipeline, update_job

urlpatterns = [
    path("jobs/", JobListView.as_view(), name="job-list"),
    path("jobs/<int:pk>/", update_job, name="job-update"),
    path("pipeline/runs/", PipelineRunListView.as_view(), name="pipeline-runs"),
    path("pipeline/run/", trigger_pipeline, name="pipeline-run"),
]
