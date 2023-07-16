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
        return "<" + str(self.id) + ", " + self.stock_code + ", " + self.stock_name + ">"
    
class sector_type(models.Model):
    id = models.AutoField(primary_key=True)

class theme_type(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.ForeignKey(sector_type, on_delete=models.CASCADE)
    theme_name = models.CharField(max_length=50, unique=True)
    theme_description = models.CharField(max_length=1000)

    def __str__(self):
        return "<" + str(self.id) + ", " + self.theme_name + ", " + self.theme_description + ">"

class upjong_type(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.ForeignKey(sector_type, on_delete=models.CASCADE)
    upjong_name = models.CharField(max_length=50, unique=True)
    upjong_description = models.CharField(max_length=1000)

    def __str__(self):
        return "<" + str(self.id) + ", " + self.upjong_name + ", " + self.upjong_description + ">"

class theme_of_stock(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.ForeignKey(theme_type, on_delete=models.CASCADE)
    stock = models.ForeignKey(stock_info, on_delete=models.CASCADE)

class upjong_of_stock(models.Model):
    id = models.AutoField(primary_key=True)
    upjong = models.ForeignKey(upjong_type, on_delete=models.CASCADE)
    stock = models.ForeignKey(stock_info, on_delete=models.CASCADE)

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
        return "<" + str(self.id) + ", " + str(self.stock) + ", " + str(self.date) + ", " \
             + str(self.open_price) + ", " + str(self.high_price) + ", " + str(self.low_price) + ", " \
             + str(self.close_price) + ", " + str(self.volume) + ">"

class money_data(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.ForeignKey(sector_type, on_delete=models.CASCADE)
    date = models.DateField(default=0, unique=True)
    cum_money = models.BigIntegerField(default=0)

class account(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100, unique=True)
    user_pw = models.CharField(max_length=100)
    birth = models.DateField(default=None)
    gender = models.CharField(max_length=1) # "m"ale or "f"emale

    def __str__(self):
        return "<" + str(self.id) + ", " + self.user_id + ", " + str(self.birth) + ", " + self.gender + ">"

class condition_list(models.Model):
    id = models.AutoField(primary_key=True)
    condition_name = models.CharField(max_length=50, unique=True)

class interested_sector(models.Model):
    id = models.AutoField(primary_key=True)
    acc = models.ForeignKey(account, on_delete=models.CASCADE)
    sector = models.ForeignKey(sector_type, on_delete=models.CASCADE)
    condition = models.ForeignKey(condition_list, on_delete=models.CASCADE)
    from_date = models.DateField(default=0)
    to_date = models.DateField(default=0)

class interested_alarm(models.Model):
    id = models.AutoField(primary_key=True)
    acc = models.ForeignKey(account, on_delete=models.CASCADE)
    interested = models.ForeignKey(interested_sector, on_delete=models.CASCADE)
    stock = models.ForeignKey(stock_info, on_delete=models.CASCADE)
    date = models.DateField(default=0)

