from django.http import HttpResponse
from django.urls import path, include
from django.views import View

from login_required import login_not_required, LoginNotRequiredMixin


@login_not_required
def sample1(request):
    return HttpResponse()


class SampleView(LoginNotRequiredMixin, View):
    def get(self, *args, **kwargs):
        return HttpResponse()


urlpatterns_with_namespace = [
    path("foo2/", lambda request: HttpResponse("foo2"), name="foo")
]

urlpatterns = [
    path("bar/", lambda request: HttpResponse("bar"), name="bar"),
    path("foo/", lambda request: HttpResponse("foo"), name="foo"),
    path("sample1/", sample1, name="sample1"),
    path("sample2/", SampleView.as_view(), name="sample2"),
    path("", include((urlpatterns_with_namespace, "app"))),
]
