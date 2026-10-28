from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Job, PipelineRun
from .serializers import JobSerializer, PipelineRunSerializer
from .services.pipeline import run_pipeline
from .tasks import run_pipeline_task

class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(application_status=status_filter)
        role = self.request.query_params.get("q")
        if role:
            from django.db.models import Q
            qs = qs.filter(Q(title__icontains=role) | Q(description__icontains=role) | Q(matched_tags__icontains=role))
        remote = self.request.query_params.get("remote")
        if remote in ("true", "false"):
            qs = qs.filter(remote=(remote == "true"))
        return qs

class PipelineRunListView(generics.ListAPIView):
    serializer_class = PipelineRunSerializer
    queryset = PipelineRun.objects.all()[:50]

@api_view(["POST"])
def trigger_pipeline(request):
    mode = request.data.get("mode", "sync")
    if mode == "async":
        task = run_pipeline_task.delay("manual")
        return Response({"task_id": task.id, "status": "queued"}, status=status.HTTP_202_ACCEPTED)
    run = run_pipeline(trigger="manual")
    return Response(PipelineRunSerializer(run).data, status=status.HTTP_200_OK if run.status == "succeeded" else status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["PATCH"])
def update_job(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({"detail": "Job not found."}, status=404)
    serializer = JobSerializer(job, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
