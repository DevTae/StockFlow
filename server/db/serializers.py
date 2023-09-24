# serializers.py
# transform django model into json type

from rest_framework import serializers
from .models import market_type, sector_type, theme_type, stock_info, theme_of_stock, \
                    price_data, account, condition_list, interested_sector, interested_alarm, money_data, \
                    indicator_sma_data

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = market_type
        fields = ("__all__")
        #fields = ('id', 'market_name')
