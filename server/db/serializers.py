# serializers.py
# transform django model into json type

from rest_framework import serializers
from .models import market_type

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = market_type
        fields = ("__all__")
        #fields = ('id', 'market_name')
