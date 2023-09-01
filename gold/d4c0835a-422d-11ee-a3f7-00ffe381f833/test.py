# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals
from gm.api import *

import datetime
import numpy as np
import pandas as pd


def init(context):

    stock = "SZSE.002475"
    start_time = "2000-05-25"
    end_time = ""

    stock_data_df = get_history_symbol(stock, start_time, end_time, True)

    stock_data_df["复权价"] = stock_data_df['pre_close'] * stock_data_df['adj_factor']

    # print(stock_data_df[stock_data_df.adj_factor > 1])
    print(stock_data_df.iloc[165])
    print(stock_data_df[stock_data_df.adj_factor > 1][['trade_date', 'adj_factor', 'pre_close', '复权价']])


if __name__ == "__main__":
    run(strategy_id='d4c0835a-422d-11ee-a3f7-00ffe381f833',
        filename='test.py',
        mode=MODE_BACKTEST,
        token='da62d7ac539fcffc1faf4a22511c1397d7dacb95',
        backtest_start_time='2020-11-01 08:00:00',
        backtest_end_time='2020-11-10 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=10000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001)