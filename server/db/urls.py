from django.urls import path, include
from .views.stock_view import MarketView, StockInfoView, StockInfoEachView
from . import tests

urlpatterns = [
    path('test/', tests.test, name='test'), # for test
    path('reset/', tests.reset, name='reset'), # for test
    
    # stock
    path('market/', MarketView.as_view(), name="market"),
    path('stock/', StockInfoView.as_view(), name="stock-list"),
    path('stock/<str:stock_code>/', StockInfoEachView.as_view(), name="stock-per"),
]
