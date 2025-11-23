from django.utils.deprecation import MiddlewareMixin
from accounts.models import VisitorIP

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class VisitorCountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = get_client_ip(request)

        if not ip:
            return

        VisitorIP.objects.get_or_create(ip_address=ip)

