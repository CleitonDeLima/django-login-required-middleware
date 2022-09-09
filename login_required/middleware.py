import re

from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.urls import resolve
from django.contrib.auth import REDIRECT_FIELD_NAME as REDIRECT_FIELD_NAME_DEFAULT

IGNORE_PATHS = [
    re.compile(url) for url in getattr(settings, "LOGIN_REQUIRED_IGNORE_PATHS", [])
]

IGNORE_VIEW_NAMES = list(getattr(settings, "LOGIN_REQUIRED_IGNORE_VIEW_NAMES", []))

REDIRECT_FIELD_NAME = getattr(settings, "LOGIN_REQUIRED_REDIRECT_FIELD_NAME", REDIRECT_FIELD_NAME_DEFAULT)


class LoginRequiredMiddleware(AuthenticationMiddleware):
    @staticmethod
    def _login_required(request):
        if request.user.is_authenticated:
            return None

        path = request.path
        if any(url.match(path) for url in IGNORE_PATHS):
            return None

        try:
            resolver = resolve(path)
        except Http404:
            return redirect_to_login(request.get_full_path())

        view_func = resolver.func

        if not getattr(view_func, "login_required", True):
            return None

        view_class = getattr(view_func, "view_class", None)
        if view_class and not getattr(view_class, "login_required", True):
            return None

        if resolver.view_name in IGNORE_VIEW_NAMES:
            return None

        return redirect_to_login(request.get_full_path(), redirect_field_name=REDIRECT_FIELD_NAME)

    def process_request(self, request):
        """
        Use process_request instead of defining __call__ directly;
        Django's middleware layer will process_request in a coroutine in __acall__ if it detects an async context.
        Otherwise, it will use __call__.
        https://github.com/django/django/blob/acde91745656a852a15db7611c08cabf93bb735b/django/utils/deprecation.py#L88-L148
        """
        return self._login_required(request)
