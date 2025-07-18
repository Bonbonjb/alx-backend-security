from django.http import JsonResponse
from ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required

# Use method='POST' for login requests
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return JsonResponse({'error': 'Too many requests'}, status=429)
    
    # Mock login logic for demonstration
    if request.method == 'POST':
        return JsonResponse({'message': 'Login successful'})
    return JsonResponse({'message': 'Send a POST request to log in'})