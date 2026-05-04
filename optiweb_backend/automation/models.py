from django.db import models

from django.db import models

class AutomationLog(models.Model):
    server_id = models.CharField(max_length=255)
    service_name = models.CharField(max_length=50)
    fix_result = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fix {self.service_name} on {self.server_id} at {self.timestamp}"
