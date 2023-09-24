from django.urls import path, include
from rest_framework import routers
from . import views
from . import tests

router = routers.DefaultRouter()
router.register('market', views.MarketViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', tests.test, name='test'),
    path('reset/', tests.reset, name='reset'),
    path('', include(router.urls)),
]
