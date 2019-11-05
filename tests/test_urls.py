from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponse

urlpatterns_with_namespace = [
    url(r'^foo2/$', lambda request: HttpResponse('foo2'), name='foo')
]

urlpatterns = [
    url(r'^bar/$', lambda request: HttpResponse('bar'), name='bar'),
    url(r'^foo/$', lambda request: HttpResponse('foo'), name='foo'),
    url(r'^admin/', admin.site.urls),
    url('', include((urlpatterns_with_namespace, 'app')))
]
