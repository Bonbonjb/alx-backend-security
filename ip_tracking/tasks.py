from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import SuspiciousIP
from django.db.models import Count
from ip_tracking.models import IPRequestLog  # Assuming you log IP requests here

SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def detect_anomalies():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # 1. Flag IPs with >100 requests/hour
    high_freq_ips = (
        IPRequestLog.objects
        .filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(request_count=Count('id'))
        .filter(request_count__gt=100)
    )

    for entry in high_freq_ips:
        ip = entry['ip_address']
        SuspiciousIP.objects.get_or_create(ip_address=ip, defaults={'reason': 'Too many requests in 1 hour'})

    # 2. Flag IPs accessing sensitive paths
    sensitive_ips = (
        IPRequestLog.objects
        .filter(path__in=SENSITIVE_PATHS, timestamp__gte=one_hour_ago)
        .values_list('ip_address', flat=True)
        .distinct()
    )

    for ip in sensitive_ips:
        SuspiciousIP.objects.get_or_create(ip_address=ip, defaults={'reason': 'Accessed sensitive path'})