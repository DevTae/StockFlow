from django.urls import path, include
from rest_framework import routers
from .views import market
from . import tests

router = routers.DefaultRouter()
router.register('market', market.MarketViewSet)

urlpatterns = [
    path('', market.index, name='index'),
    path('test/', tests.test, name='test'), # for test
    path('reset/', tests.reset, name='reset'), # for test
    path('', include(router.urls)),
]
