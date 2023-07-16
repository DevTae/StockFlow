# Developed by DevTae@2023
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from .models import sector_type, theme_type, upjong_type, theme_of_stock, price_data, money_data, interested_sector, interested_alarm

# theme_type 새롭게 insert 할 시, sector_type 에 반영
@receiver(pre_save, sender=theme_type)
def add_sector_type(sender, instance, **kwargs):
    if instance.id == None:
        new_sector_type = sector_type.objects.create()
        instance.sector_id = new_sector_type.id
    
# upjong_type 새롭게 insert 할 시, sector_type 에 반영
@receiver(pre_save, sender=upjong_type)
def add_sector_type(sender, instance, **kwargs):
    if instance.id == None:
        new_sector_type = sector_type.objects.create()
        instance.sector_id = new_sector_type.id

# price_data 가 수정되는 경우, 다음과 같은 처리 진행
@receiver(pre_save, sender=price_data)
def pre_save_price_data(sender, instance, **kwargs):
    # update 인 경우, 누적 거래대금에서 제외함
    if instance.id != None:
        previous_instance = price_data.objects.get(id=instance.id)
        multiple_theme_of_stock = theme_of_stock.objects.filter(stock_id=instance.stock)
        for single_theme_of_stock in multiple_theme_of_stock:
            sector = single_theme_of_stock.theme.sector
            money = money_data.objects.get(sector=sector.id, date=previous_instance.date)
            money.cum_money -= previous_instance.close_price * previous_instance.volume # 임의 계산
            if money.cum_money == 0:
                money.delete()
            else:
                money.save()

# price_data 가 수정되는 경우, 다음과 같은 처리 진행
# 1. 속하는 섹터에 대한 누적 거래대금 반영
# 2. (insert 일 때,) 기간 내 관심등록한 테마에 대한 종목일 때, 일정 트리거를 만족하면 알람 등록
@receiver(post_save, sender=price_data)
def post_save_price_data(sender, instance, created, **kwargs):
    # insert 일 때
    if created:
        # 기간 내 관심등록한 테마에 대한 종목일 때, 일정 트리거를 만족하면 알림 등록
        pass

    # 속하는 테마의 거래대금에 누적합을 반영함
    multiple_theme_of_stock = theme_of_stock.objects.filter(stock_id=instance.stock)
    for single_theme_of_stock in multiple_theme_of_stock:
        sector = single_theme_of_stock.theme.sector
        try:
            money = money_data.objects.get(sector=sector.id, date=instance.date)
            money.cum_money += instance.close_price * instance.volume # 임의 계산
        except:
            money = money_data()
            money.sector = sector
            money.date = instance.date
            money.cum_money = instance.close_price * instance.volume
        finally:
            money.save()

    # 속하는 섹터의 거래대금에 누적합을 반영함
    pass

# price_data 가 삭제되는 경우, 다음과 같은 처리 진행
# 1. 속하는 섹터에 대한 누적 거래대금 반영
@receiver(pre_delete, sender=price_data)
def post_delete_price_data(sender, instance, **kwargs):
    # 속하는 테마의 거래대금에 누적합을 반영함
    multiple_theme_of_stock = theme_of_stock.objects.filter(stock_id=instance.stock)
    for single_theme_of_stock in multiple_theme_of_stock:
        sector = single_theme_of_stock.theme.sector
        money = money_data.objects.get(sector=sector.id, date=instance.date)
        money.cum_money -= instance.close_price * instance.volume
        if money.cum_money == 0:
            money.delete()
        else:
            money.save()
