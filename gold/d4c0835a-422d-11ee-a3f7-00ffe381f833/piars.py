# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals
from gm.api import *

import datetime
import numpy as np
import pandas as pd


def init(context):

    stock1 = "SHSE.513330"
    # stock2 = "SHSE.513060"
    stock2 = "SZSE.159742"

    start_time = "2021-05-25"
    end_time = ""

    stock1_data_df = get_history_symbol(stock1, start_time, end_time, True)
    stock2_data_df = get_history_symbol(stock2, start_time, end_time, True)

    stock1_prices = stock1_data_df['pre_close']
    stock2_prices = stock2_data_df['pre_close']
    # print(stock2_data_df)

    r = np.corrcoef(stock1_prices, stock2_prices)

    print("相关性系数：", r)


if __name__ == "__main__":
    run(strategy_id='d4c0835a-422d-11ee-a3f7-00ffe381f833',
        filename='piars.py',
        mode=MODE_BACKTEST,
        token='da62d7ac539fcffc1faf4a22511c1397d7dacb95',
        backtest_start_time='2020-11-01 08:00:00',
        backtest_end_time='2020-11-10 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=10000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001)