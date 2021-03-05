from django.apps import AppConfig


class LoginRequiredConfig(AppConfig):
    name = "login_required"

    def ready(self):
        from django.contrib.auth import views

        login_not_required_views = (
            views.LoginView,
            views.PasswordResetView,
            views.PasswordResetDoneView,
            views.PasswordResetConfirmView,
            views.PasswordResetCompleteView,
        )
        for view in login_not_required_views:
            view.login_required = False
