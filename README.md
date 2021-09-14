django-login-required-middleware
==============

![Tests](https://github.com/CleitonDeLima/django-login-required-middleware/workflows/Tests/badge.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/CleitonDeLima/django-login-required-middleware/badge.svg)](https://coveralls.io/github/CleitonDeLima/django-login-required-middleware?branch=master)
[![PyPI Version](https://img.shields.io/pypi/v/django-login-required-middleware.svg)](https://pypi.org/project/django-login-required-middleware/)
[![PyPI downloads](https://img.shields.io/pypi/dm/django-login-required-middleware.svg)](https://img.shields.io/pypi/dm/django-login-required-middleware.svg)


**django-login-required-middleware** provide login to all requests through middleware.

If the website has many views and almost all use
`LoginRequiredMixin` or the `login_required` decorator, using `django-login-required`
can keep the code of your views more clear and avoids forgetting authentication of view.

Requirements
------------

* **Python**: 3.6, 3.7, 3.8
* **Django**: 1.11, 2.0, 2.1, 2.2, 3.0x

Quick start
-----------

1. Install `pip install django-login-required-middleware`
2. Add `login_required.middleware.LoginRequiredMiddleware` to `MIDDLEWARE` after
`django.contrib.auth.middleware.AuthenticationMiddleware`
3. (Optional) To ignore authentication in a view uses decorato `@login_not_required` for FBV or `LoginNotRequiredMixin` for CBV:

    ```python
    from login_required import login_not_required

    @login_not_required
    def my_view(request):
        return HttpResponse()
    ```

    or

    ```python
    from login_required import LoginNotRequiredMixin

    class MyView(LoginNotRequiredMixin, View):
        def get(self, request, *args, **kwargs):
            return HttpResponse()
    ```

4. (Optional) Add `LOGIN_REQUIRED_IGNORE_PATHS` setting.
Any requests which match these paths will be ignored. This setting should be a list filled with
regex paths (`settings.LOGIN_URL` always included).

    Example:

    ```python
    LOGIN_REQUIRED_IGNORE_PATHS = [
        r'/accounts/logout/$'
        r'/accounts/signup/$',
        r'/admin/$',
        r'/about/$'
    ]
    ```

5. (Optional) Add `LOGIN_REQUIRED_IGNORE_VIEW_NAMES` setting.
Any requests which match these url name will be ignored. This setting should be a list filled with
url names.

    Example:

    ```python
    LOGIN_REQUIRED_IGNORE_VIEW_NAMES = [
        'home',
        'admin:index',
        'admin:login',
        'namespace:url_name',
    ]
    ```
