# Copyright DevTae@2023 all rights reserved.
from django.db import models

class market_type(models.Model):
    id = models.AutoField(primary_key=True)
    market_name = models.CharField(max_length=20, unique=True)

class stock_info(models.Model):
    id = models.AutoField(primary_key=True)
    stock_code = models.CharField(max_length=6, unique=True)
    stock_name = models.CharField(max_length=50)
    market = models.ForeignKey(market_type, on_delete=models.CASCADE)
    
    def __str__(self):
        return "<stock_info: " + str(self.id) + ", " + self.stock_code + ", " + self.stock_name + ">"
 
class price_data(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(stock_info, on_delete=models.CASCADE)
    date = models.DateField(default=0)
    open_price = models.FloatField(default=0)
    high_price = models.FloatField(default=0)
    low_price = models.FloatField(default=0)
    close_price = models.FloatField(default=0)
    volume = models.FloatField(default=0)
    shares = models.BigIntegerField(default=0)
    market_cap = models.BigIntegerField(default=0)

    def __str__(self):
        return "<price_data: " + str(self.id) + ", " + str(self.stock) + ", " + str(self.date) + ", " \
             + str(self.open_price) + ", " + str(self.high_price) + ", " + str(self.low_price) + ", " \
             + str(self.close_price) + ", " + str(self.volume) + ">"

# 가격예측 결과 지표 모델 추가
class price_predicted_data(models.Model):
    price = models.ForeignKey(price_data, on_delete=models.CASCADE)
    score = models.IntegerField(default=50) # 0 ~ 100
