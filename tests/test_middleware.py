import re

import mock
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from login_required.middleware import LoginRequiredMiddleware

User = get_user_model()


class LoginRequiredMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = LoginRequiredMiddleware()
        self.user = User.objects.create_user(username='test')
        self.request = self.factory.get('/foo/')
        self.request.user = self.user

    def test_authentication_middleware_required(self):
        del self.request.user

        with self.assertRaises(AssertionError):
            self.middleware.process_request(self.request)

    def test_redirect_to_login(self):
        response = self.client.get('/foo/')
        self.assertEqual(response.status_code, 302)

    def test_normal_redirect_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get('/foo/')

        self.assertEqual(response.status_code, 200)

    @mock.patch(
        'login_required.middleware.IGNORE_PATHS', [re.compile(r'^/foo/$')]
    )
    def test_ignore_path_config(self):
        response = self.client.get('/foo/')
        self.assertEqual(response.status_code, 200)

    @mock.patch('login_required.middleware.IGNORE_VIEW_NAMES', ['foo'])
    def test_ignore_url_names_config(self):
        response = self.client.get('/foo/')
        self.assertEqual(response.status_code, 200)

    @mock.patch('login_required.middleware.IGNORE_VIEW_NAMES', ['app:foo'])
    def test_ignore_url_names_with_namespace_config(self):
        response = self.client.get('/foo2/')
        self.assertEqual(response.status_code, 200)

    @mock.patch('login_required.middleware.IGNORE_VIEW_NAMES', ['bar'])
    def test_ignore_url_names_another_name_config(self):
        response = self.client.get('/foo/')
        self.assertEqual(response.status_code, 302)

    @mock.patch('login_required.middleware.IGNORE_VIEW_NAMES', ['foo'])
    def test_ignore_url_names_invalid_path_call_config(self):
        response = self.client.get('/bar/')
        self.assertEqual(response.status_code, 302)

    def test_ajax_request(self):
        response = self.client.get('/foo/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)
