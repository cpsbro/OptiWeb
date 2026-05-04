import json
import joblib
import numpy as np
from django.http import JsonResponse
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

# Load the trained model
MODEL_PATH = "ml_api/enhanced_failure_predictor_model.pkl"
model = joblib.load(MODEL_PATH)

class PredictFailureView(APIView):
    """API endpoint to predict server failure risk and send alerts."""

    def get_user_email(self, server_id):
        """Fetch user email associated with the given server_id from the database."""
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT email FROM authentication_user WHERE web_server_ip = %s", [server_id]
            )
            row = cursor.fetchone()
        return row[0] if row else None  # Return email if found, otherwise None

    def post(self, request):
        try:
            data = request.data
            server_id = data.get("server_id", "Unknown Server")

            # Fetch user email associated with this server
            user_email = self.get_user_email(server_id)

            if not user_email:
                print(f"? No email found for server {server_id}, skipping alert.")
                return Response({"message": "No email found for this server"}, status=status.HTTP_400_BAD_REQUEST)

            # Extract input features
            input_features = [
                float(data.get("cpu_usage", 0)),
                float(data.get("memory_usage", 0)),
                float(data.get("disk_usage", 0)),
                float(data.get("uptime", 0)),
                int(data.get("web_500_errors", 0)),
                int(data.get("web_404_errors", 0)),
                int(data.get("web_ssl_errors", 0)),
                int(data.get("web_slow_response_warnings", 0)),
                int(data.get("web_resource_limit_warnings", 0)),
                int(data.get("db_connection_failures", 0)),
                int(data.get("db_auth_failures", 0)),
                int(data.get("db_deadlocks", 0)),
                int(data.get("db_out_of_memory", 0)),
                int(data.get("db_slow_queries", 0)),
                int(data.get("db_connection_limits", 0))
            ]

            # Predict failure risk
            input_data = np.array([input_features])
            prediction = model.predict(input_data)
            failure_risk = bool(prediction[0])

            # Generate reasons for high/low risk
            reasons = []
            if input_features[0] > 85:
                reasons.append("?? High CPU usage detected")
                failure_risk = True
            if input_features[1] > 90:
                reasons.append("?? High memory usage detected")
                failure_risk = True
            if input_features[2] > 95:
                reasons.append("?? High disk usage detected")
                failure_risk = True
            if input_features[4] > 5:
                reasons.append("? Multiple 500 Internal Server Errors detected")
                failure_risk = True
            if input_features[9] > 3:
                reasons.append("? Multiple database connection failures detected")
                failure_risk = True

            # Check Web & Database Service Status
            web_service_status = json.loads(data.get("web_service_status", "{}"))
            db_service_status = json.loads(data.get("db_service_status", "{}"))

            web_down_services = [service for service, status in web_service_status.items() if status == "inactive"]
            db_down_services = [service for service, status in db_service_status.items() if status == "inactive"]

            if web_down_services:
                reasons.append(f"? Web Service(s) Down: {', '.join(web_down_services)}")
                failure_risk = True  # Ensure HIGH risk if web service is down
            if db_down_services:
                reasons.append(f"? Database Service(s) Down: {', '.join(db_down_services)}")
                failure_risk = True  # Ensure HIGH risk if DB service is down

            # Include error logs if available
            logs = data.get("logs", "[]")
            log_entries = json.loads(logs)
            error_logs = [log for log in log_entries if "error" in log.lower() or "failed" in log.lower()]

            if error_logs:
                reasons.append(f"? Error Logs Detected: {', '.join(error_logs[:3])}...")

            # Response payload
            response = {
                "server_id": server_id,
                "failure_risk": failure_risk,
                "reasons": reasons if reasons else ["? No major issues detected"],
            }

            # If High Risk ? Send Email Alert
            if failure_risk:
                subject = f"?? High Risk Alert: {server_id}"
                message = f"""
                Alert: High failure risk detected for server: {server_id}
                
                Reasons:
                - {chr(10).join(reasons)}
                
                Immediate action is required to prevent service failure.
                """
                send_mail(
                    subject,
                    message,
                    "no-reply@optiweb.com",  # Change this to your sender email
                    [user_email],
                    fail_silently=False,
                )
                print(f"? Email alert sent to {user_email} for server {server_id}")

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
