from django.test import TestCase
from django.http import HttpResponse

from .models.stock import market_type, stock_info, price_data, price_predicted_data
from .models.sector import sector_type, theme_type, theme_of_stock
from .models.money import money_data
import datetime

# 해당 코드들 Fat Model 및 Service Layer 로서 구현. (기본적인 함수 호출은 Fat Model 편입 생각 중)
# 추가적인 함수 구현. (ex. get_stock_instance)
# PK 찾는 부분에서 데이터베이스 반복 접근에 대한 비효율적인 현상을 개선하기 위하여 HashMap, LRU 등의 알고리즘을 적용.

# 섹터 인스턴스 반환 함수
def get_sector_instance(theme: theme_type):
    return theme.sector

# 주식 번호를 바탕으로 주식 PK 찾기
def get_stock_id(stock_code):
    selected_stock = stock_info.objects.get(stock_code=stock_code)
    return selected_stock.id

# 테마 이름을 바탕으로 테마 PK 찾기
def get_theme_id(theme_name):
    selected_theme = theme_type.objects.get(theme_name=theme_name)
    return selected_theme.id

# 테마 이름을 바탕으로 섹터 PK 찾기
def get_sector_id_from_theme(theme_name: str):
    selected_theme = theme_type.objects.get(theme_name=theme_name)
    return selected_theme.sector

# 테마 PK 를 바탕으로 섹터 PK 찾기
def get_sector_id_from_theme(theme_id: int):
    selected_theme = theme_type.objects.get(theme_id=theme_id)
    return selected_theme.sector

"""
# 유저 아이디를 바탕으로 유저 인스턴스 찾기
def get_account_id(user_id):
    selected_account = account.objects.get(user_id=user_id)
    return selected_account

# 조건 이름을 바탕으로 조건 인스턴스 찾기
def get_condition_id(condition_name):
    selected_condition = condition_list.objects.get(condition_name=condition_name)
    return selected_condition
"""

def insert_market(market_id, market_name):
    new_market = market_type()
    new_market.id = market_id
    new_market.market_name = market_name
    new_market.save()
    return new_market

def insert_theme(name, description):
    new_theme_type = theme_type()
    new_theme_type.theme_name = name
    new_theme_type.theme_description = description
    new_theme_type.save()
    return new_theme_type

def update_theme(before_name, after_name, after_description):
    selected = theme_type.objects.get(theme_name=before_name)
    selected.theme_name = after_name
    selected.theme_description = after_description
    selected.save()
    return selected

def insert_stock(market_id, stock_code, stock_name):
    new_stock = stock_info()
    new_stock.market = market_id
    new_stock.stock_code = stock_code
    new_stock.stock_name = stock_name
    new_stock.save()
    return new_stock

# 주식 PK, 테마 PK 를 바탕으로 주식 테마 편입
def insert_stock_into_theme(stock, theme):
    new_theme_of_stock = theme_of_stock()
    new_theme_of_stock.stock = stock
    new_theme_of_stock.theme = theme
    new_theme_of_stock.save()
    return new_theme_of_stock

"""
def insert_account(user_id, user_pw, birth, gender):
    new_account = account()
    new_account.user_id = user_id
    new_account.user_pw = user_pw
    new_account.birth = birth
    new_account.gender = gender
    new_account.save()
    return new_account

def insert_condition(condition_id, condition_name):
    new_condition = condition_list()
    new_condition.id = condition_id
    new_condition.condition_name = condition_name
    new_condition.save()
    return new_condition

def insert_stock_into_interested(account, sector, condition_id, from_date, to_date):
    new_interested_sector = interested_sector()
    new_interested_sector.acc = account
    new_interested_sector.sector = sector
    new_interested_sector.condition = condition_id
    new_interested_sector.from_date = from_date
    new_interested_sector.to_date = to_date
    new_interested_sector.save()
    return new_interested_sector
"""

def insert_price_data(stock, date, open_price, high_price, low_price, close_price, volume, shares, market_cap):
    new_price_data = price_data()
    new_price_data.stock = stock
    new_price_data.date = date
    new_price_data.open_price = open_price
    new_price_data.high_price = high_price
    new_price_data.low_price = low_price
    new_price_data.close_price = close_price
    new_price_data.volume = volume
    new_price_data.shares = shares
    new_price_data.market_cap = market_cap
    new_price_data.save()
    return new_price_data

def insert_price_predicted_data(price, score):
    new_price_predicted_data = price_predicted_data()
    new_price_predicted_data.price = price
    new_price_predicted_data.score = score
    new_price_predicted_data.save()
    return new_price_predicted_data

"""
def insert_indicator_sma_data(price, period, value):
    new_indicator_sma_data = indicator_sma_data()
    new_indicator_sma_data.price = price
    new_indicator_sma_data.period = period
    new_indicator_sma_data.value = value
    new_indicator_sma_data.save()
    return new_indicator_sma_data
"""

def update_price_data(stock, date, open_price, high_price, low_price, close_price, volume, shares, market_cap):
    new_price_data = price_data.objects.get(stock=stock, date=date)
    new_price_data.open_price = open_price
    new_price_data.high_price = high_price
    new_price_data.low_price = low_price
    new_price_data.close_price = close_price
    new_price_data.volume = volume
    new_price_data.shares = shares
    new_price_data.market_cap = market_cap
    new_price_data.save()
    return new_price_data

def delete_price_data(stock, date):
    try:
        selected = price_data.objects.get(stock=stock.id, date=date)
        selected.delete()
    except:
        print("not found")

def test(request):
    # 새로운 시장 생성
    market = insert_market(1, "kospi")
    print(market_type.objects.all())

    # 새로운 테마 생성
    theme = insert_theme("it service", "the most revolution of technology in the world")
    sector = get_sector_instance(theme)
    print(theme_type.objects.all())

    # 종목 추가 및 테마에 종목 추가
    stock_1 = insert_stock(market, "005930", "삼성전자")
    stock_2 = insert_stock(market, "009150", "삼성전기")
    print(stock_info.objects.all())
    insert_stock_into_theme(stock_1, theme)
    insert_stock_into_theme(stock_2, theme)
    print(theme_of_stock.objects.all())

    """
    # 조건검색 기준 추가
    condition = insert_condition(1, "과열")
    print(condition_list.objects.all())

    # 유저 가입 및 관심 등록
    acc = insert_account("id", "pw", datetime.date(2010, 2, 3), "m")
    print(account.objects.all())
    insert_stock_into_interested(acc, sector, condition, datetime.date(2023, 7, 10), datetime.date(2023, 7, 31))
    print(interested_sector.objects.all())
    """
    
    # 종목에 가격 데이터 추가
    price_data_1_1 = insert_price_data(stock_1, datetime.date(2023, 7, 11), 70200, 71500, 70100, 71500, 12177392, 0, 0)
    price_data_1_2 = insert_price_data(stock_1, datetime.date(2023, 7, 12), 70200, 71500, 70100, 71500, 12177392, 0, 0)
    price_data_2_1 = insert_price_data(stock_2, datetime.date(2023, 7, 11), 140200, 145300, 139900, 145300, 378816, 0, 0)
    price_data_2_2 = insert_price_data(stock_2, datetime.date(2023, 7, 12), 140200, 145300, 139900, 145300, 378816, 0, 0)
    print(str(price_data.objects.all()))
    for money in money_data.objects.all():
        print(str(money.sector) + ", " + str(money.date) + ", " + str(money.cum_money))

    # 가격예측 데이터 추가
    price_predicted_data_1_1 = insert_price_predicted_data(price_data_1_1, 30)
    price_predicted_data_1_2 = insert_price_predicted_data(price_data_1_2, 70)
    print(str(price_predicted_data.objects.all()))

    """
    # 종목 가격 데이터에 보조지표 추가
    indicator_sma_data_1_1_20 = insert_indicator_sma_data(price_data_1_1, 20, 71000)
    indicator_sma_data_1_1_60 = insert_indicator_sma_data(price_data_1_1, 60, 71500)
    indicator_sma_data_1_2_20 = insert_indicator_sma_data(price_data_1_1, 20, 140000)
    print(str(indicator_sma_data.objects.all()))
    """

    # 가격 데이터 업데이트
    price_data_1_1 = update_price_data(stock_1, datetime.date(2023, 7, 11), 100000, 100000, 100000, 100000, 12177392, 0, 0)
    price_data_2_1 = update_price_data(stock_2, datetime.date(2023, 7, 11), 140200, 145300, 139900, 200000, 378816, 0, 0)
    print(str(price_data.objects.all()))
    for money in money_data.objects.all():
        print(str(money.sector) + ", " + str(money.date) + ", " + str(money.cum_money))

    # 가격 데이터 제거
    delete_price_data(stock_1, datetime.date(2023, 7, 11))
    print(str(price_data.objects.all()))
    for money in money_data.objects.all():
        print(str(money.sector) + ", " + str(money.date) + ", " + str(money.cum_money))

    # 종목 제거 및 거래대금 누적합 확인
    stock_1.delete()
    stock_2.delete()
    print(str(price_data.objects.all()))
    for money in money_data.objects.all():
        print(str(money.sector) + ", " + str(money.date) + ", " + str(money.cum_money))
    print(str(price_predicted_data.objects.all()))
    #print(str(indicator_sma_data.objects.all()))

    return HttpResponse("Done.")

def reset(request):
    market_type.objects.all().delete()
    sector_type.objects.all().delete()
    theme_type.objects.all().delete()
    stock_info.objects.all().delete()
    theme_of_stock.objects.all().delete()
    price_data.objects.all().delete()
    price_predicted_data.objects.all().delete()
    """
    account.objects.all().delete()
    condition_list.objects.all().delete()
    interested_sector.objects.all().delete()
    interested_alarm.objects.all().delete()
    indicator_sma_data.objects.all().delete()
    """

    return HttpResponse("Done.")
