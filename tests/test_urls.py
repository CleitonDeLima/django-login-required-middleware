from django.urls import path, include
from django.contrib import admin
from django.http import HttpResponse

urlpatterns_with_namespace = [
    path('foo2/', lambda request: HttpResponse('foo2'), name='foo')
]

urlpatterns = [
    path('bar/', lambda request: HttpResponse('bar'), name='bar'),
    path('foo/', lambda request: HttpResponse('foo'), name='foo'),
    path('admin/', admin.site.urls),
    path('', include((urlpatterns_with_namespace, 'app'))),
]
