from django.db import models

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField()
    path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp} - {self.path}"