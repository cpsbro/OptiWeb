from django.core.mail import send_mail
import json

def send_alert_email(server_id, failure_risk, reasons, recipient_email):
    """Send an email alert when a high failure risk is detected."""
    if failure_risk:  # ? Only send email if failure risk is HIGH
        subject = f"?? High Failure Risk Alert for Server {server_id}"
        message = f"""
        Attention,

        The AI prediction system has detected a HIGH failure risk for server: {server_id}

        **Reasons:**
        {', '.join(reasons)}

        Please investigate immediately.

        Best,
        OptiWeb Monitoring System
        """

        try:
            send_mail(
                subject,
                message,
                'www.chameeraprabhath1998@gmail.com',  # ? Your sender email
                [recipient_email],  # ? Receiver email
                fail_silently=False,
            )
            print(f"? Alert email sent to {recipient_email} for server {server_id}")
        except Exception as e:
            print(f"? Error sending alert email: {e}")
