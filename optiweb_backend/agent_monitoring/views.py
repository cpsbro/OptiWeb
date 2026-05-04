import json
from django.db.models import Max
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ServerMetrics
from .serializers import ServerMetricsSerializer

class AgentMetricsView(APIView):
    def post(self, request):
        data = request.data
        server_id = data.get("server_id")

        try:
            # Parse incoming service status
            web_services = json.loads(data.get("web_service_status", "{}"))
            db_services = json.loads(data.get("db_service_status", "{}"))

            # Store only installed services
            filtered_web_services = {k: v for k, v in web_services.items() if v is not None}
            filtered_db_services = {k: v for k, v in db_services.items() if v is not None}

            # Save metrics data
            metrics = ServerMetrics.objects.create(
                server_id=server_id,
                cpu_usage=data["cpu_usage"],
                memory_usage=data["memory_usage"],
                disk_usage=data["disk_usage"],
                uptime=data["uptime"],
                logs=json.dumps(data["logs"]),
                web_service_status=json.dumps(filtered_web_services),
                db_service_status=json.dumps(filtered_db_services)
            )

            return Response({"message": "Metrics received successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        latest_metrics = (
            ServerMetrics.objects.values("server_id")
            .annotate(latest_timestamp=Max("timestamp"))
            .order_by("-latest_timestamp")
        )

        latest_metrics_entries = ServerMetrics.objects.filter(
            timestamp__in=[entry["latest_timestamp"] for entry in latest_metrics]
        ).order_by("-timestamp")

        serializer = ServerMetricsSerializer(latest_metrics_entries, many=True)
        return Response(serializer.data)
