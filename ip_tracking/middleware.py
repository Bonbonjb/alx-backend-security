from django.http import HttpResponseForbidden
from django.utils.timezone import now
from ipware import get_client_ip
from django.core.cache import cache
import requests
from .models import RequestLog, BlockedIP

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        timestamp = now()
        path = request.path

        if ip:
            # Check if IP is blocked
            if BlockedIP.objects.filter(ip_address=ip).exists():
                return HttpResponseForbidden("403 Forbidden: Your IP has been blocked.")

            # Get geolocation (cached for 24 hours)
            location = cache.get(ip)
            if not location:
                location = self.get_geolocation(ip)
                cache.set(ip, location, timeout=86400)  # Cache for 24 hours

            # Log request with location
            RequestLog.objects.create(
                ip_address=ip,
                timestamp=timestamp,
                path=path,
                country=location.get('country'),
                city=location.get('city')
            )

        return self.get_response(request)

    def get_geolocation(self, ip):
        try:
            response = requests.get(f'https://ipapi.co/{ip}/json/')
            if response.status_code == 200:
                data = response.json()
                return {
                    'country': data.get('country_name'),
                    'city': data.get('city')
                }
        except requests.RequestException:
            pass
        return {'country': None, 'city': None}