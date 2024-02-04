from rest_framework import serializers
from ..models.stock_model import market_type, stock_info


class MarketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = market_type
        fields = ("id", "market_name")

class StockInfoSerializer(serializers.ModelSerializer):
    market_name = serializers.SerializerMethodField() # "market_name" 에 대한 속성

    class Meta:
        model = stock_info
        fields = ("id", "market", "market_name", "stock_code", "stock_name")

    def get_market_name(self, obj):
        return obj.market.market_name