import re

import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from login_required.middleware import LoginRequiredMiddleware

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='test')


def test_authentication_middleware_required(user):
    factory = RequestFactory()
    middleware = LoginRequiredMiddleware()
    request = factory.get('/foo/')
    request.user = user
    del request.user

    with pytest.raises(AssertionError):
        middleware.process_request(request)


def test_redirect_to_login(client):
    response = client.get('/foo/')
    assert response.status_code == 302


def test_normal_redirect_authenticated(client, user):
    client.force_login(user)
    response = client.get('/foo/')

    assert response.status_code == 200


def test_ignore_path_config(client, mocker):
    mocker.patch(
        'login_required.middleware.IGNORE_PATHS', [re.compile(r'^/foo/$')]
    )
    response = client.get('/foo/')

    assert response.status_code == 200


def test_ignore_url_names_config(client, mocker):
    mocker.patch('login_required.middleware.IGNORE_VIEW_NAMES', ['foo', 'bar'])
    response = client.get('/bar/')

    assert response.status_code == 200


def test_ignore_url_names_with_namespace_config(client, mocker):
    mocker.patch('login_required.middleware.IGNORE_VIEW_NAMES', ['app:foo'])
    response = client.get('/foo2/')

    assert response.status_code == 200


def test_ignore_url_names_another_name_config(client, mocker):
    mocker.patch('login_required.middleware.IGNORE_VIEW_NAMES', ['bar'])
    response = client.get('/foo/')

    assert response.status_code == 302


def test_ignore_url_names_invalid_path_call_config(client, mocker):
    mocker.patch('login_required.middleware.IGNORE_VIEW_NAMES', ['foo'])
    response = client.get('/bar/')

    assert response.status_code == 302


def test_raise_404(client):
    response = client.get('/nonexistent-url/')

    assert response.status_code == 404
