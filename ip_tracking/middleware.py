from django.utils.timezone import now
from ipware import get_client_ip
from .models import RequestLog

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        timestamp = now()
        path = request.path

        if ip:
            RequestLog.objects.create(
                ip_address=ip,
                timestamp=timestamp,
                path=path
            )

        return self.get_response(request)