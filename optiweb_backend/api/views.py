from rest_framework.views import APIView
from rest_framework.response import Response

class MetricsView(APIView):
    def get(self, request):
        # Simulate dynamic metrics or get them from your system
        metrics = [
            {"title": "CPU Usage", "value": "34%"},
            {"title": "Memory Usage", "value": "60%"},
            {"title": "Disk Space", "value": "80%"},
            {"title": "Network", "value": "Good"},
        ]
        return Response(metrics)
