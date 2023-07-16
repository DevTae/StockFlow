from django.urls import path
from . import views
from . import tests

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', tests.test, name='test'),
    path('reset/', tests.reset, name='reset')
]
