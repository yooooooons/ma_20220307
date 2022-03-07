#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pyupbit
import datetime
import pandas as pd
import numpy as np
import warnings

#from scipy.signal import savgol_filter
#from scipy.signal import savitzky_golay

import matplotlib.pyplot as plt


# In[2]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)


# In[3]:


invest_ratio = 0.015   # 보유 금액의 최대 몇 % 를 투자할것인가 (예> 0.1 <-- 보유금액 10% 투자) 

# 투자 대상 코인
coin_No = 1
coin_inv = 'KRW-ETH'
check_currency = 'KRW'



candle_type = '60min'
candle_count = 70

#몇 일 기준 이동평균선을 구할것인가
mv_avg_duration_1 = 35
mv_avg_duration_2 = 35

# close 가격 변동 비율에 따른 매수 / 매도 결정
close_ratio_buy_cri = 1.0001
close_ratio_sell_cri = 0.9999

mv_avg_ratio_buy_cri = 1.0001
mv_avg_ratio_sell_cri = 0.9999


# 거래량이 평상시의 몇 배 이상일시 매수
volume_buy = 1 * 1.52
volume_sell = volume_buy * 1

'''
#candle_type = '60min'
candle_type = '3min'
candle_count = 50

#몇 일 기준 이동평균선을 구할것인가
#mv_avg_duration_1 = 35
mv_avg_duration_1 = 5
mv_avg_duration_2 = 35

# close 가격 변동 비율에 따른 매수 / 매도 결정
close_ratio_buy_cri = 0.999
close_ratio_sell_cri = 1.1

mv_avg_ratio_buy_cri = 0.999
mv_avg_ratio_sell_cri = 1.1


# 거래량이 평상시의 몇 배 이상일시 매수
volume_buy = 1 * 0.3
volume_sell = volume_buy * 1
'''


# 매수시 몇 가격 unit 까지 상향해서 구매할 것인가
#buy_price_up_unit = 3

# 거래 수수료 비율
transaction_fee_ratio = 0.0005   # 거래 수수료 비율

sell_drop_ratio_force = 0.03   # 강제 매도 하락율
transaction_fee_ratio = 0.0005   # 거래 수수료 비율

time_factor = 9   # 클라우드 서버와 한국과의 시차


# In[4]:



if candle_type == '1min' :
    candle_adapt = 'minute1'
    time_unit = 1
elif candle_type == '3min' :
    candle_adapt = 'minute3'
    time_unit = 3
elif candle_type == '5min' :
    candle_adapt = 'minute5'
    time_unit = 5
elif candle_type == '10min' :
    candle_adapt = 'minute10'
    time_unit = 10
elif candle_type == '15min' :
    candle_adapt = 'minute15'
    time_unit = 15
elif candle_type == '30min' :
    candle_adapt = 'minute30'
    time_unit = 30
elif candle_type == '60min' :
    candle_adapt = 'minute60'
    time_unit = 60
elif candle_type == '240min' :
    candle_adapt = 'minute240'
    time_unit = 240


# In[5]:


'''
# 투자 대상 코인
#coin_No = 2
coin_inv = 'KRW-NEO'
check_currency = 'KRW'

candle_type = '5min'
#candle_adapt = 'minute5'
#candle_count = int(60/5) * 24 * 365
candle_count = 50

#몇 일 기준 이동평균선을 구할것인가
mv_avg_duration_1 = 8
mv_avg_duration_2 = mv_avg_duration_1 * 3

#몇 개 연속 하락일시 투자를 결정?
#series_0_buy_cnt_No = 1
#series_0_sell_cnt_No = 1

# close 가격 변동 비율에 따른 매수 / 매도 결정
close_ratio_buy_cri = 1.0005
close_ratio_sell_cri = 0.9995

# 거래량이 평상시의 몇 배 이상일시 매수
volume_buy = 1 * 2

# 매수시 몇 가격 unit 까지 상향해서 구매할 것인가
buy_price_up_unit = 3

#test_money = 1000000

#buy_time_value = 29000
#sell_time_value = 28000

transaction_fee_ratio = 0.0005   # 거래 수수료 비율


invest_ratio = 0.015   # 보유 금액의 최대 몇 % 를 투자할것인가 (예> 0.1 <-- 보유금액 10% 투자) 

#buy_time_value = 2
#sell_time_value = 1
#idle_time_value = 0

sell_drop_ratio_force = 0.03   # 강제 매도 하락율
transaction_fee_ratio = 0.0005   # 거래 수수료 비율

time_factor = 9   # 클라우드 서버와 한국과의 시차


if candle_type == '1min' :
    candle_adapt = 'minute1'
    time_unit = 1
elif candle_type == '3min' :
    candle_adapt = 'minute3'
    time_unit = 3
elif candle_type == '5min' :
    candle_adapt = 'minute5'
    time_unit = 5
elif candle_type == '10min' :
    candle_adapt = 'minute10'
    time_unit = 10
elif candle_type == '15min' :
    candle_adapt = 'minute15'
    time_unit = 15
elif candle_type == '30min' :
    candle_adapt = 'minute30'
    time_unit = 30
elif candle_type == '60min' :
    candle_adapt = 'minute60'
    time_unit = 60
elif candle_type == '240min' :
    candle_adapt = 'minute240'
    time_unit = 240
'''


# In[6]:


access_key = "eziU49y9cSYp6BFEu8Vu8yEwk0AAZIxn1o0ya7Bp"
secret_key = "mjkWq13cmg1XE38l9xK7x80XhcIsyChHrmyx3IVe"

upbit = pyupbit.Upbit(access_key, secret_key)


# In[7]:


tickers = pyupbit.get_tickers()

LIST_coin_KRW = []

for i in range (0, len(tickers), 1):
    if tickers[i][0:3] == 'KRW':
        LIST_coin_KRW.append(tickers[i])

LIST_check_coin_currency = []

for i in range (0, len(LIST_coin_KRW), 1):
    LIST_check_coin_currency.append(LIST_coin_KRW[i][4:])

LIST_check_coin_currency_2 = []

for i in range (0, len(LIST_check_coin_currency), 1) :
    temp = 'KRW-' + LIST_check_coin_currency[i]
    LIST_check_coin_currency_2.append(temp)


# In[8]:


LIST_check_coin_currency[coin_No]


# In[9]:


# 잔고 조회, 현재가 조회 함수 정의

def get_balance(target_currency):   # 현급 잔고 조회
    """잔고 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_balance_locked(target_currency):   # 거래가 예약되어 있는 잔고 조회
    """잔고 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['locked'] is not None:
                return float(b['locked'])
            else:
                return 0
    return 0

def get_avg_buy_price(target_currency):   # 거래가 예약되어 있는 잔고 조회
    """평균 매수가 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0
    return 0


def get_current_price(invest_coin):
    """현재가 조회"""
    #return pyupbit.get_orderbook(tickers=invest_coin)[0]["orderbook_units"][0]["ask_price"]
    return pyupbit.get_current_price(invest_coin)

#price = pyupbit.get_current_price("KRW-BTC")


# In[10]:


def moving_avg_trend (DF_input) :
    Series_moving_avg_1 = DF_input['close'].rolling(window = mv_avg_duration_1).mean()
    Series_moving_avg_2 = DF_input['close'].rolling(window = mv_avg_duration_2).mean()
    
    DF_moving_avg_1 = Series_moving_avg_1.to_frame(name='close_mv_avg_1')
    DF_moving_avg_2 = Series_moving_avg_2.to_frame(name='close_mv_avg_2')
    
    #DF_moving_avg_1['prior_close_mv_avg_1'] = DF_moving_avg_1['close_mv_avg_1'].shift(1)
    DF_moving_avg_1['ratio_mv_avg_1'] = DF_moving_avg_1['close_mv_avg_1'] / DF_moving_avg_1['close_mv_avg_1'].shift(1)
    
    #DF_moving_avg_2['prior_close_mv_avg_2'] = DF_moving_avg_2['close_mv_avg_2'].shift(1)
    DF_moving_avg_2['ratio_mv_avg_2'] = DF_moving_avg_2['close_mv_avg_2'] / DF_moving_avg_2['close_mv_avg_2'].shift(1)
    
    #DF_input['prior_close'] = DF_input['close'].shift(1)
    DF_input['ratio_close'] = DF_input['close'] / DF_input['close'].shift(1)
    
    DF_concat = pd.concat([DF_input,DF_moving_avg_1],axis=1)
    DF_concat = pd.concat([DF_concat,DF_moving_avg_2],axis=1)
    
    volume_avg = DF_concat['volume'].mean()
    DF_concat['ratio_volume'] = DF_concat['volume'] / volume_avg

    return DF_concat


# In[11]:


DF_temp = pyupbit.get_ohlcv(coin_inv, count = candle_count, interval = candle_adapt)


# In[12]:


#DF_temp


# In[13]:


if DF_temp['open'][0] >= 1000000 :  # 200만원 이상은 거래단위가 1000원, 100~200만원은 거래단위가 500원이지만 편의상 200만원 이상과 함께 처리
    unit_factor = -3
    unit_value = 1000
elif DF_temp['open'][0] >= 100000 :
    unit_factor = -2
    unit_value = 50
elif DF_temp['open'][0] >= 10000 :
    unit_factor = -1
    unit_value = 10
elif DF_temp['open'][0] >= 1000 :
    unit_factor = -1
    unit_value = 5
elif DF_temp['open'][0] >= 100 :
    unit_factor = 0
    unit_value = 1
else :
    DF_temp['open'][0] <= 100   # 100원 미만은 별도로 code에서 int형이 아닌 float형으로 형변환 해줘야함
    unit_factor = 1
    unit_value = 0.1

print ('DF_temp[open][0] : {0}  / unit_value : {1}'.format(DF_temp['open'][0], unit_value))


# In[14]:


bought_state = 0
bought_price = 0


# In[ ]:


while True:
    
    now = datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600))   # 클라우드 서버와 한국과의 시간차이 보정 (9시간)
    print ('bought_state : {0}   / now : {1}'.format(bought_state, now))
    
    if (now.minute % time_unit == 0) & (55 < (now.second % 60) <= 59) :   # N시:00:02초 ~ N시:00:07초 사이 시각이면
        balances = upbit.get_balances()
        print ('current_aseet_status\n', balances)
        
        if bought_state == 0 :   # 매수가 없는 상태라면
            DF_invest_check = DF_inform = pyupbit.get_ohlcv(coin_inv, count = candle_count, interval = candle_adapt)
            DF_mov_avg_check = moving_avg_trend (DF_invest_check)
            print('DF_mov_avg_check :\n', DF_mov_avg_check)
            print('close_ratio_buy_cri : {0}  / DF_mov_avg_check[ratio_close][-2] : {1}'.format(close_ratio_buy_cri, DF_mov_avg_check['ratio_close'][-2]))
            print('ratio_mv_avg_1 : {0} / DF_mov_avg_check[ratio_mv_avg_1][-2] : {1}'.format(mv_avg_ratio_buy_cri, DF_mov_avg_check['ratio_mv_avg_1'][-2]))
            print('ratio_volume : {0} / DF_mov_avg_check[ratio_volume][-2] : {1}'.format(volume_buy, DF_mov_avg_check['ratio_volume'][-2]))
            
            # 매수 영역
            if ((DF_mov_avg_check['ratio_close'][-2] > close_ratio_buy_cri) & (DF_mov_avg_check['ratio_mv_avg_1'][-2] > mv_avg_ratio_buy_cri) & (DF_mov_avg_check['ratio_volume'][-2] > volume_buy)) :
                print ('$$$$$ [{0}] buying_transaction is coducting $$$$$'.format(coin_inv))
                    
                investable_budget = get_balance(check_currency) * invest_ratio
                bought_volume = (investable_budget * (1 - transaction_fee_ratio)) / get_current_price(coin_inv)
                currrent_price = get_current_price(coin_inv)
                
                print ('investable_budget : {0} / currrent_price : {1} / bought_volume : {2}'.format(investable_budget, currrent_price, bought_volume))
                
                #transaction_buy = upbit.buy_market_order(coin_inv, investable_budget)   # 시장가로 매수
                transaction_buy1 = upbit.buy_limit_order(coin_inv, currrent_price, bought_volume)   # 지정가로 매수
                time.sleep(10)
                print ('buy_1ST_transaction_result :', transaction_buy1)
                print ('time : {0}  /  bought_target_volume : {1}  /  bought_volume_until_now : {2}'.format((datetime.datetime.now() + datetime.timedelta(seconds = (time_factor*3600))), bought_volume, get_balance(coin_inv[4:])))
                
                if get_balance(coin_inv[4:]) <= (0.95 *bought_volume) :
                    volume_diff = bought_volume - get_balance(coin_inv[4:])
                    transaction_buy2 = upbit.buy_limit_order(coin_inv, (currrent_price + (1 * unit_value)), bought_volume)   # 지정가로 매수
                    time.sleep(10)
                    print ('buy_2ND_transaction_result :', transaction_buy2)
                    print ('time : {0}  /  bought_target_volume : {1}  /  bought_volume_until_now : {2}'.format((datetime.datetime.now() + datetime.timedelta(seconds = (time_factor*3600))), bought_volume, get_balance(coin_inv[4:])))
                    if get_balance(coin_inv[4:]) <= (0.95 *bought_volume) :
                        volume_diff2 = bought_volume - get_balance(coin_inv[4:])
                        transaction_buy3 = upbit.buy_limit_order(coin_inv, (currrent_price + (2 * unit_value)), bought_volume)   # 지정가로 매수
                        time.sleep(10)
                        print ('buy_3RD_transaction_result :', transaction_buy3)
                        print ('time : {0}  /  bought_target_volume : {1}  /  bought_volume_until_now : {2}'.format((datetime.datetime.now() + datetime.timedelta(seconds = (time_factor*3600))), bought_volume, get_balance(coin_inv[4:])))
                        
                        if get_balance(coin_inv[4:]) <= (0.95 *bought_volume) :
                            now2 = datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600))   # 클라우드 서버와 한국과의 시간차이 보정 (9시간)
                            
                            while (0 <= (now2.minute % time_unit) <= 10) :   # 0분에서 10분 사이면
                                bought_price = upbit.get_balances()[coin_inv]['avg_buy_price']
                                if get_current_price(coin_inv) <= (bought_price * (1-sell_drop_ratio_force)) :   # 강제 매도 가격 이하로 현재가격이 하락하게 되면
                                    transaction_sell = upbit.sell_market_order(coin_inv, get_balance(coin_inv[4:0]))   # 시장가에 매도
                                    time.sleep(5)
                                    print ('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds = (time_factor*3600))))
                                    print ('sell_transaction_result_BY_FORCED_SELLING_in the WHILE_loop :', transaction_sell)
                                
                                time.sleep(1)                                
                        
                        if get_balance(coin_inv[4:]) <= (0.95 *bought_volume) :
                            transaction_buy_cancel1 = upbit.cancel_order(transaction_buy1['uuid'])
                            transaction_buy_cancel2 = upbit.cancel_order(transaction_buy2['uuid'])
                            transaction_buy_cancel3 = upbit.cancel_order(transaction_buy3['uuid'])
                            print('\n [Some or All transaction_buy is NOT conducted with some reason at {0}]'.format(now - datetime.timedelta(seconds=10)))
                    
                    transaction_buy_cancel1 = upbit.cancel_order(transaction_buy1['uuid'])
                    transaction_buy_cancel2 = upbit.cancel_order(transaction_buy2['uuid'])
                    
                transaction_buy_cancel1 = upbit.cancel_order(transaction_buy1['uuid'])
                
                
                   
    # 매수 상태 점검
    if get_balance(coin_inv[4:]) > 0 :
        bought_state = 1
        print ('bought_state_in mid check : {0}'.format(bought_state))
    else : 
        bought_state = 0
        print ('bought_state_in mid check : {0}'.format(bought_state))
 
                    
    #매도 영역
    if (now.minute % time_unit == 0) & (55 < (now.second % 60) <= 59) :   # N시:00:02초 ~ N시:00:07초 사이 시각이면
        balances2 = upbit.get_balances()
        print ('current_aseet_status\n', balances2)
        
        if bought_state == 1 :   # 매수가 되어 있는 상태라면
            print ('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds = (time_factor*3600))))
            print ('\n bought_state : {0}  [[[[[[[[[[[[ coin___{1} selling condition checking]]]]]]]]]] :'.format(bought_state, coin_inv))
            DF_invest_check_SELL = pyupbit.get_ohlcv(coin_inv, count = candle_count, interval = candle_adapt)
            DF_mov_avg_check_SELL = moving_avg_trend (DF_invest_check_SELL)
            print ('mv_avg_ratio_sell_cri : {0}  / DF_mov_avg_check_SELL[ratio_mv_avg_1][-2]  : {1}'.format(mv_avg_ratio_sell_cri, DF_mov_avg_check_SELL['ratio_mv_avg_1'][-2]))
            print ('volume_sell : {0}  / DF_mov_avg_check_SELL[ratio_volume][-2]  : {1}'.format(volume_sell, DF_mov_avg_check_SELL['ratio_volume'][-2]))
            
            if (DF_mov_avg_check_SELL['ratio_mv_avg_1'][-2] <= mv_avg_ratio_sell_cri) & (DF_mov_avg_check_SELL['ratio_volume'][-2] > volume_sell):                                
                transaction_sell = upbit.sell_market_order(coin_inv, get_balance(coin_inv[4:]))   # 시장가에 매도
                time.sleep(5)
                print ('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds = (time_factor*3600))))
                print ('sell_transaction_result_BY_NORMAL_SELLING :', transaction_sell)
                
                bought_state = 0
                
                time.sleep(5)
        
        
    # 하락시 강제 매도 영역
    if bought_state == 1 :   # 매수가 되어 있는 상태라면
            
        if get_current_price(coin_inv) <= (bought_price * (1-sell_drop_ratio_force)) :   # 강제 매도 가격 이하로 현재가격이 하락하게 되면
            
            transaction_sell = upbit.sell_market_order(coin_inv, get_balance(coin_inv[4:0]))   # 시장가에 매도
            time.sleep(5)
            print ('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds = (time_factor*3600))))
            print ('sell_transaction_result_BY_FORCED_SELLING :', transaction_sell)
            bought_state = 0
            time.sleep(5)
        
    time.sleep(1)
    


# In[ ]:





# In[ ]:


get_current_price('KRW-NEO')


# In[ ]:


get_balance ('KRW')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




