from rest_framework import serializers
from .models import Trace


class TraceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trace
        exclude = ['is_deleted', 'modified_at', 'created_at']
