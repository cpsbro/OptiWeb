from django.db import models

class ServerMetrics(models.Model):
    server_id = models.CharField(max_length=255)
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()
    uptime = models.FloatField()
    logs = models.TextField()

    # Updated fields to store longer JSON data
    web_service_status = models.TextField(default="{}")  # Store JSON as string
    db_service_status = models.TextField(default="{}")

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('server_id', 'timestamp')

    def __str__(self):
        return f"Metrics for {self.server_id} at {self.timestamp}"
  