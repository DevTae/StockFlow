# Copyright DevTae@2023 all rights reserved.
from django.db import models
from .sector_model import sector_type

# 누적 거래대금 지표 모델 추가
class money_data(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.ForeignKey(sector_type, on_delete=models.CASCADE)
    date = models.DateField(default=0, unique=True)
    cum_money = models.BigIntegerField(default=0)
