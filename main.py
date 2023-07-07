import sys
import os
# from scrapy.cmdline import execute
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy', 'crawl', 'sync_history_nev'])


# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 Double Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

import requests
import json
import os


import numpy as np
import pandas as pd
# import matplotlib as mpl
import matplotlib.pyplot as plt
# import matplotlib.dates as m_date

def get_count(data):
    sort_data_before = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0,
                        "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0,
                        "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0, "28": 0, "29": 0, "30": 0,
                        "31": 0, "32": 0, "33": 0, "34": 0, "35": 0}
    sort_data_after = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0,
                       "11": 0, "12": 0}
    for item in data:
        for date_item in str.split(item['lotteryDrawResult'],  " ")[:-2]:
            sort_data_before[date_item] += 1
        for date_item in str.split(item['lotteryDrawResult'],  " ")[-2:]:
            sort_data_after[date_item] += 1
    return sort_data_before, sort_data_after


def __ema(self, n, last_ema, current_price):
    return (2 * current_price + (n - 1) * last_ema)/(n + 1)


def _ma(close_prices, n):
    close_prices = np.array(close_prices)
    ma = []
    for index in range(1, len(close_prices)):
        start = index - n if index - n >= 0 else 0
        count = index - start
        ma.append(np.average(close_prices[start:index]))
    return ma

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':

    data_count = 1500

    response = requests.get("https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize="+ str(data_count) +"&isVerify=1&pageNo=1")
    response_data = json.loads(response.text)
    data = response_data['value']['list']
    sort_data = ""
    before = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35"]
    after = ["01","02","03","04","05","06","07","08","09","10","11","12"]

    for i in range(len(data)):
        item = data[i]
        sort_data += item['lotteryDrawNum'] + "," + str.replace(item['lotteryDrawResult'],  " ",  ",") + "\n"

    data = data[2:]
    data = data[::-1]

    print(data[-1]['lotteryDrawNum'])

    m = 50
    n = 50
    st = 1
    sort_data_before = []
    sort_data_after = []
    date_stage = []
    date_index = []

    for i0 in range(len(before)):
        sort_data_before.append([])
    for i1 in range(len(after)):
        sort_data_after.append([])

    all_before_ma = []
    all_after_ma = []
    all_before_count, all_after_count = get_count(data)
    for i0 in range(len(before)):
        all_before_ma.append(all_before_count[before[i0]]/(data_count*5))
    for i1 in range(len(after)):
        all_after_ma.append(all_after_count[after[i1]]/(data_count*2))

    all_before_ma_list = []
    all_after_ma_list = []
    for i0 in range(len(before)):
        all_before_ma_list.append([])
    for i1 in range(len(after)):
        all_after_ma_list.append([])

    for i in range(len(data)):
        item = data[i]
        if m <= i < len(data) and (i % st == 0 or i == len(data) - 1):
            sort_data_before_item, sort_data_after_item = get_count(data[i-m:i])
            date_stage.append(item['lotteryDrawNum'])
            date_index.append(i)
            for i0 in range(len(before)):
                sort_data_before[i0].append(sort_data_before_item[before[i0]]/(m * 5))
                all_before_ma_list[i0].append(all_before_ma[i0])
            for i1 in range(len(after)):
                sort_data_after[i1].append(sort_data_after_item[after[i1]]/(m * 2))
                all_after_ma_list[i1].append(all_after_ma[i1])

    # print(date_stage[-1])
    # print(all_before_ma)
    # print(all_before_ma[2])
    # exit()

    print("before:")
    for i0 in range(len(before)):
        item_ma_list = _ma(sort_data_before[i0], n)
        data_speed = pd.DataFrame(item_ma_list).pct_change(periods=1, fill_method="pad")
        if np.array(data_speed)[-1] < 0:
            print(before[i0])

        dot_count = 200
        # plt.figure(figsize=((dot_count / 80) * 13, 8))
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=((dot_count / 80) * 13, 16))
        ax1.scatter(range(len(sort_data_before[i0])), sort_data_before[i0], c="#cccccc", linewidths=1)
        ax1.plot(all_before_ma_list[i0], linestyle="-", color="#F52D2D", linewidth=2)
        ax1.plot(item_ma_list, linestyle="-", color="#ababab", linewidth=2)

        ax2.plot(np.array(data_speed), linestyle="-", color="#F52D2D", linewidth=2)
        ax2.plot((np.zeros((len(data_speed),), dtype=int)), linestyle="-", color="#000000", linewidth=2)

        plt.xlabel("before:" + before[i0])
        plt.savefig("./data/caipiao/before_" + before[i0] + ".jpg", format="jpg", bbox_inches="tight", pad_inches=0,
                    transparent=True, dpi=32)
        plt.axis("off")
        plt.clf()
        plt.close("all")

    print("after:")
    for i1 in range(len(after)):
        item_ma_list = _ma(sort_data_after[i1], n)
        data_speed = pd.DataFrame(item_ma_list).pct_change(periods=1, fill_method="pad")
        if (np.array(data_speed)[-1] < 0 or np.array(data_speed)[-2] < 0) \
                and (item_ma_list[-1] - all_after_ma[i1]) < 0:
            print(after[i1])

        dot_count = 200
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=((dot_count / 80) * 13, 16))
        ax1.scatter(range(len(sort_data_after[i1])), sort_data_after[i1], c="#cccccc")
        ax1.plot(all_after_ma_list[i1], linestyle="-", color="#F52D2D", linewidth=2)
        ax1.plot(item_ma_list, linestyle="-", color="#ababab", linewidth=4)

        ax2.plot(np.array(data_speed), linestyle="-", color="#F52D2D", linewidth=2)
        ax2.plot((np.zeros((len(data_speed),), dtype=int)), linestyle="-", color="#000000", linewidth=2)

        plt.xlabel("after:" + after[i1])
        plt.savefig("./data/caipiao/after_" + after[i1] + ".jpg", format="jpg", bbox_inches="tight", pad_inches=0,
                    transparent=True, dpi=32)
        plt.axis("off")
        plt.clf()
        plt.close("all")

    file_path = os.path.dirname(os.path.realpath(__file__)) + "/data/caipiao/sort_data.csv"
    with open(file_path,  "w",  encoding="utf8") as fp:
        fp.write(sort_data)
        fp.close()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
