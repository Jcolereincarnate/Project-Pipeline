from rest_framework import serializers
from .models import Job, PipelineRun

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ("source_post_id", "source", "discovered_at", "last_seen_at")

class PipelineRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = PipelineRun
        fields = "__all__"
