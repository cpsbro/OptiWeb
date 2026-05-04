import json
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import AutomationLog
from agent_monitoring.models import ServerMetrics
from rest_framework.authentication import TokenAuthentication


class FixIssueView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        server_id = data.get("server_id")
        fixes_data = data.get("fixes")

        # ? AGENT: Sends fixes
        if server_id and fixes_data:
            try:
                fixes = json.loads(fixes_data)
                for service, result in fixes.items():
                    AutomationLog.objects.create(
                        server_id=server_id,
                        service_name=service,
                        fix_result=result
                    )
                return Response({"message": "Fixes logged successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=400)

        # ? FRONTEND: Manual fix by user
        user = request.user
        server_id = getattr(user, 'web_server_ip', None)

        if not server_id:
            return Response({"error": "No server ID found for user"}, status=400)

        try:
            latest_metrics = ServerMetrics.objects.filter(server_id=server_id).order_by("-timestamp").first()
            if not latest_metrics:
                return Response({"error": "No recent metrics found"}, status=404)

            web_services = json.loads(latest_metrics.web_service_status)
            db_services = json.loads(latest_metrics.db_service_status)
            all_services = {**web_services, **db_services}
        except Exception as e:
            return Response({"error": f"Error retrieving metrics: {e}"}, status=400)

        fix_results = {}
        for service, status_val in all_services.items():
            if status_val == "inactive":
                try:
                    result = subprocess.run(["systemctl", "restart", service], capture_output=True, text=True)
                    msg = (
                        f"{service} restarted successfully." if result.returncode == 0
                        else f"Failed to restart {service}."
                    )
                except Exception as e:
                    msg = f"Error restarting {service}: {str(e)}"

                fix_results[service] = msg
                AutomationLog.objects.create(
                    server_id=server_id,
                    service_name=service,
                    fix_result=msg
                )

        return Response({
            "message": "Manual auto-fix complete.",
            "fix_results": fix_results
        }, status=200)

    def get(self, request):
        return Response({"error": "GET not allowed on this endpoint."}, status=405)


class GetAutomationLogsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        server_id = getattr(user, 'web_server_ip', None)

        if not server_id:
            return Response({"error": "Server ID not found"}, status=400)

        logs = AutomationLog.objects.filter(server_id=server_id).order_by("-timestamp")[:10]
        log_data = [
            {
                "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "service_name": log.service_name,
                "fix_result": log.fix_result,
            } for log in logs
        ]
        return Response(log_data, status=200)
