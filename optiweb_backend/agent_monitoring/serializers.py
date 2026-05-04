from rest_framework import serializers
from .models import ServerMetrics

class ServerMetricsSerializer(serializers.ModelSerializer):
    web_service_status = serializers.JSONField()
    db_service_status = serializers.JSONField()

    class Meta:
        model = ServerMetrics
        fields = '__all__'
