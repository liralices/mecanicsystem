from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_paths = (
            '/login/',
            '/registrar/',
            '/logout/',
            '/admin/',
            '/static/',
            '/media/',
        )

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if not any(path.startswith(path_prefix) for path_prefix in self.allowed_paths):
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)
