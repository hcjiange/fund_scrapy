# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals
from gm.api import *

import matplotlib.pyplot as plt  # 导入包
import datetime
import numpy as np
import pandas as pd

'''
配对交易策略
'''


def init(context):
    context.stock1 = "SHSE.513330"
    context.stock2 = "SZSE.159742"

    context.start_time = "2021-05-25"
    context.end_date = ""
    # 权重阈值
    context.Threshold_weight = 0.0035
    # 定时任务，日频
    # schedule(schedule_func=algo, date_rule='1d', time_rule='15:00:00')
    # prices = get_history_symbol(symbol=context.index_symbol, start_date="2020-01-01", df=True)
    # print(prices["trade_date"])
    # algo(context)
    # 定时任务，日频
    schedule(schedule_func=algo, date_rule='1d', time_rule='15:00:00')
    # algo(context)


def algo(context):

    end_date = str(context.now)[0:10]
    data_stock1 = get_history_symbol(symbol=context.stock1, start_date=context.start_time, end_date=end_date, df=True)
    data_stock2 = get_history_symbol(symbol=context.stock2, start_date=context.start_time, end_date=end_date, df=True)

    price_stock1 = data_stock1['pre_close']
    price_stock2 = data_stock2['pre_close']
    # fig = plt.figure()  # 创建空图
    # plt.plot(data_stock1['trade_date'], price_stock1, color='r', linewidth=1.0, linestyle='--')
    # plt.plot(data_stock2['trade_date'], price_stock2, color='b', linewidth=1.0, linestyle='--')
    # plt.show()  # 将图形显示出来

    diff = price_stock1 - price_stock2

    up = np.mean(diff) + np.std(diff)
    down = np.mean(diff) - np.std(diff)

    last_diff = price_stock1.iloc[-1] - price_stock2.iloc[-1]

    total_money = int(context.account(account_id=None).cash['nav'])

    new_price1 = current(symbols=context.stock1)[0]['price']
    new_price2 = current(symbols=context.stock2)[0]['price']
    if last_diff > up:
        order_value(symbol=context.stock1, value=total_money, side=OrderSide_Sell,
                           order_type=OrderType_Market, position_effect=PositionEffect_Close)
        order_value(symbol=context.stock2, value=total_money, side=OrderSide_Buy,
                           order_type=OrderType_Market, position_effect=PositionEffect_Open)
    if last_diff < down:
        order_value(symbol=context.stock2, value=total_money, side=OrderSide_Sell,
                           order_type=OrderType_Market, position_effect=PositionEffect_Close)
        order_value(symbol=context.stock1, value=total_money, side=OrderSide_Buy,
                           order_type=OrderType_Market, position_effect=PositionEffect_Open)

    print(end_date, new_price1, last_diff, up, down, total_money)

    # up_list = np.ones(len(diff)) * (np.mean(diff) + np.std(diff))
    # down_list = np.ones(len(diff)) * (np.mean(diff) - np.std(diff))
    # fig = plt.figure()  # 创建空图
    # plt.plot(data_stock1['trade_date'], diff, color='r', linewidth=1.0, linestyle='--')
    # plt.plot(data_stock1['trade_date'], up_list, color='b', linewidth=1.0, linestyle='--')
    # plt.plot(data_stock1['trade_date'], down_list, color='b', linewidth=1.0, linestyle='--')
    # plt.show()  # 将图形显示出来


def on_order_status(context, order):
    # 标的代码
    symbol = order['symbol']
    # 委托价格
    price = order['price']
    # 委托数量
    volume = order['volume']
    # 目标仓位
    target_percent = order['target_percent']
    # 查看下单后的委托状态，等于3代表委托全部成交
    status = order['status']
    # 买卖方向，1为买入，2为卖出
    side = order['side']
    # 开平仓类型，1为开仓，2为平仓
    effect = order['position_effect']
    # 委托类型，1为限价委托，2为市价委托
    order_type = order['order_type']
    if status == 3:
        if effect == 1:
            if side == 1:
                side_effect = '开多仓'
            else:
                side_effect = '开空仓'
        else:
            if side == 1:
                side_effect = '平空仓'
            else:
                side_effect = '平多仓'
        order_type_word = '限价' if order_type == 1 else '市价'
        print('{}:标的：{}，操作：以{}{}，委托价格：{}，委托数量：{}'.format(context.now, symbol, order_type_word, side_effect, price,
                                                         volume))


if __name__ == '__main__':
    '''
        strategy_id策略ID, 由系统生成
        filename文件名, 请与本文件名保持一致
        mode运行模式, 实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID, 可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式, 不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
        '''
    run(strategy_id='d4c0835a-422d-11ee-a3f7-00ffe381f833',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='da62d7ac539fcffc1faf4a22511c1397d7dacb95',
        backtest_start_time='2022-10-25 08:00:00',
        backtest_end_time='2023-08-25 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=10000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001)

