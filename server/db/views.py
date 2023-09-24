from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import MarketSerializer
from .models import market_type, sector_type, theme_type, stock_info, theme_of_stock, \
                    price_data, account, condition_list, interested_sector, interested_alarm, money_data, \
                    indicator_sma_data

def index(request):
    return HttpResponse("Hello, world.")

class MarketViewSet(viewsets.ModelViewSet):
    queryset = market_type.objects.all()
    serializer_class = MarketSerializer
