import re

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve, Resolver404

IGNORE_PATHS = [re.compile(settings.LOGIN_URL)]
IGNORE_PATHS += [
    re.compile(url)
    for url in getattr(settings, 'LOGIN_REQUIRED_IGNORE_PATHS', [])
]

IGNORE_VIEW_NAMES = [
    name
    for name in getattr(settings, 'LOGIN_REQUIRED_IGNORE_VIEW_NAMES', [])
]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), (
            'The LoginRequiredMiddleware requires authentication middleware '
            'to be installed. Edit your MIDDLEWARE setting to insert before '
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )

        path = request.path
        if not request.user.is_authenticated:

            if request.is_ajax():
                raise PermissionDenied()

            for name in IGNORE_VIEW_NAMES:
                try:
                    resolver = resolve(path)
                    if resolver.view_name == name:
                        return None
                    else:
                        return redirect_to_login(path)
                except Resolver404:
                    return redirect_to_login(path)

            if not any(url.match(path) for url in IGNORE_PATHS):
                return redirect_to_login(path)
