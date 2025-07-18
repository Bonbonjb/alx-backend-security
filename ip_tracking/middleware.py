from django.http import HttpResponseForbidden
from django.utils.timezone import now
from ipware import get_client_ip
from .models import RequestLog, BlockedIP

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        timestamp = now()
        path = request.path

        if ip:
            # Block if IP is blacklisted
            if BlockedIP.objects.filter(ip_address=ip).exists():
                return HttpResponseForbidden("403 Forbidden: Your IP has been blocked.")

            # Log request
            RequestLog.objects.create(
                ip_address=ip,
                timestamp=timestamp,
                path=path
            )

        return self.get_response(request)