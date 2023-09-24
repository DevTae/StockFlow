from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from ..serializers.market import MarketSerializer
from ..models.stock import market_type

def index(request):
    return HttpResponse("Hello, world.")

class MarketViewSet(viewsets.ModelViewSet):
    queryset = market_type.objects.all()
    serializer_class = MarketSerializer
