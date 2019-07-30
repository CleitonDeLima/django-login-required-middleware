from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = [
    url(r'^foo/$', lambda request: HttpResponse('foo')),
    url(r'^admin/', admin.site.urls),
]
