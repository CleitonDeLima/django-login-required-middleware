django-login-required-middleware
==============

**django-login-required-middleware** provide login to all requests through middleware.

If the website has many views and almost all use 
`LoginRequiredMixin` or the `login_required` decorator, using `django-login-required` 
can keep the code of your views more clear and avoids forgetting authentication of view.

Requirements
------------

* **Python**: 3.6, 3.7
* **Django**: 1.11, 2.0, 2.1, 2.2

Quick start
-----------

1. Install `pip install django-login-required-middleware`
2. Add `'login_required'` in your `INSTALLED_APPS` setting.
3. Add `login_required.middleware.LoginRequiredMiddleware` to `MIDDLEWARE` after 
`django.contrib.auth.middleware.AuthenticationMiddleware`

4. (Optional) Add `LOGIN_REQUIRED_IGNORE_PATHS` setting.  
Any requests which match these paths will be ignored. This setting should be a list filled with 
regex paths (`settings.LOGIN_URL` always included).    

Example:

```python
LOGIN_REQUIRED_IGNORE_PATHS = [
    r'accounts/logout/$'
    r'accounts/signup/$',
    r'about/$'
]
```

