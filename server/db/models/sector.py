# Copyright DevTae@2023 all rights reserved.
from django.db import models
from ..models.stock import stock_info

class sector_type(models.Model):
    id = models.AutoField(primary_key=True)

class theme_type(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.ForeignKey(sector_type, on_delete=models.CASCADE)
    theme_name = models.CharField(max_length=50, unique=True)
    theme_description = models.CharField(max_length=1000)

    def __str__(self):
        return "<theme_type: " + str(self.id) + ", " + self.theme_name + ", " + self.theme_description + ">"

class upjong_type(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.ForeignKey(sector_type, on_delete=models.CASCADE)
    upjong_name = models.CharField(max_length=50, unique=True)
    upjong_description = models.CharField(max_length=1000)

    def __str__(self):
        return "<upjong_type: " + str(self.id) + ", " + self.upjong_name + ", " + self.upjong_description + ">"

class theme_of_stock(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.ForeignKey(theme_type, on_delete=models.CASCADE)
    stock = models.ForeignKey(stock_info, on_delete=models.CASCADE)

class upjong_of_stock(models.Model):
    id = models.AutoField(primary_key=True)
    upjong = models.ForeignKey(upjong_type, on_delete=models.CASCADE)
    stock = models.ForeignKey(stock_info, on_delete=models.CASCADE)
