import re

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    LoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import RequestFactory
from login_required.middleware import LoginRequiredMiddleware

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="test")


class TestMiddleware:
    def test_user_required(self, user):
        factory = RequestFactory()
        middleware = LoginRequiredMiddleware(lambda req: HttpResponse())
        request = factory.get("/foo/")
        request.user = user
        del request.user

        with pytest.raises((AttributeError, ImproperlyConfigured)):
            middleware.process_request(request)

    def test_redirect_to_login(self, client):
        response = client.get("/foo/")
        assert response.status_code == 302

    def test_normal_redirect_authenticated(self, client, user):
        client.force_login(user)
        response = client.get("/foo/")

        assert response.status_code == 200

    def test_redirect_404(self, client):
        client.force_login(user_obj)
        response = client.get("/nonexistent-url/")

        assert response.status_code == 404


class TestIgnorePaths:
    def test_ignore_path_config(self, client, mocker):
        mocker.patch("login_required.middleware.IGNORE_PATHS", [re.compile(r"^/foo/$")])
        response = client.get("/foo/")

        assert response.status_code == 200

    def test_ignore_path_nonexistent(self, client, mocker):
        mocker.patch("login_required.middleware.IGNORE_PATHS", [re.compile(r"^/nonexistent-url/$")])
        response = client.get("/nonexistent-url/")

        assert response.status_code == 404


class TestIgnoreViewByName:
    def test_ignore_url_names_config(self, client, mocker):
        mocker.patch("login_required.middleware.IGNORE_VIEW_NAMES", ["foo", "bar"])
        response = client.get("/bar/")

        assert response.status_code == 200

    def test_ignore_url_names_with_namespace_config(self, client, mocker):
        mocker.patch("login_required.middleware.IGNORE_VIEW_NAMES", ["app:foo"])
        response = client.get("/foo2/")

        assert response.status_code == 200

    def test_ignore_url_names_another_name_config(self, client, mocker):
        mocker.patch("login_required.middleware.IGNORE_VIEW_NAMES", ["bar"])
        response = client.get("/foo/")

        assert response.status_code == 302

    def test_ignore_url_names_invalid_path_call_config(self, client, mocker):
        mocker.patch("login_required.middleware.IGNORE_VIEW_NAMES", ["foo"])
        response = client.get("/bar/")

        assert response.status_code == 302


class TestLoginRequiredAttr:
    def test_with_decorator(self, client):
        response = client.get("/sample1/")
        assert response.status_code == 200

    def test_with_mixin(self, client):
        response = client.get("/sample2/")
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "view",
        [
            LoginView,
            PasswordResetView,
            PasswordResetDoneView,
            PasswordResetConfirmView,
            PasswordResetCompleteView,
        ],
    )
    def test_login_view_with_attr_login_required(self, view):
        assert hasattr(view, "login_required")
