import re

from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.views import redirect_to_login
from django.urls import resolve

IGNORE_PATHS = [re.compile(settings.LOGIN_URL)]
IGNORE_PATHS += [
    re.compile(url) for url in getattr(settings, "LOGIN_REQUIRED_IGNORE_PATHS", [])
]

IGNORE_VIEW_NAMES = [
    name for name in getattr(settings, "LOGIN_REQUIRED_IGNORE_VIEW_NAMES", [])
]


class LoginRequiredMiddleware(AuthenticationMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            return

        if not getattr(view_func, "login_required", True):
            return None

        view_class = getattr(view_func, "view_class", None)
        if view_class and not getattr(view_class, "login_required", True):
            return None

        path = request.path
        resolver = resolve(path)
        ignore_view = resolver.view_name in IGNORE_VIEW_NAMES

        if not ignore_view and not any(url.match(path) for url in IGNORE_PATHS):
            return redirect_to_login(path)
