# Developed by DevTae@2023
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import sector_type, theme_type, upjong_type, price_data

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
# 1. 속하는 섹터에 대한 누적 거래대금 반영
# 2. (insert 일 때,) 관심등록한 테마에 대한 종목일 때, 일정 트리거를 만족하면 알람 등록
@receiver(post_save, sender=price_data)
def post_save_price_data(sender, instance, created, **kwargs):
    # insert 일 때
    if created:
        pass
    # update 일 때
    else:
        pass

# price_data 가 삭제되는 경우, 다음과 같은 처리 진행
# 1. 속하는 섹터에 대한 누적 거래대금 반영
@receiver(post_delete, sender=price_data)
def post_delete_price_data(sender, instance, **kwargs):
    pass
