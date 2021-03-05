default_app_config = "login_required.apps.LoginRequiredConfig"


def login_not_required(view_func):
    """
    Decorator for views that marks that the view is accessible by
    unauthenticated users.
    """
    view_func.login_required = False
    return view_func


class LoginNotRequiredMixin:
    """
    Mixin for CBV that marks that the view is accessible by
    unauthenticated users.
    """

    login_required = False
