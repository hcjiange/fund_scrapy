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
    response = requests.get("https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=1500&isVerify=1&pageNo=1")
    response_data = json.loads(response.text)
    data = response_data['value']['list']
    sort_data = ""
    before = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35"]
    after = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    # sort_data_before = {"01": [], "02": [], "03": [], "04": [], "05": [], "06": [], "07": [], "08": [], "09": [], "10": [], "11": [], "12": [], "13": [], "14": [], "15": [], "16": [], "17": [], "18": [], "19": [], "20": [], "21": [], "22": [], "23": [], "24": [], "25": [], "26": [], "27": [], "28": [], "29": [], "30": [], "31": [], "32": [], "33": [], "34": [], "35": 0}
    # sort_data_after = {"01": [], "02": [], "03": [], "04": [], "05": [], "06": [], "07": [], "08": [], "09": [], "10": [], "11": [], "12": []}
    unsort_data = ""
    m = 100
    st = 10
    sort_data_before = []
    sort_data_after = []
    for i0 in range(len(before)):
        sort_data_before.append([])
    for i1 in range(len(after)):
        sort_data_after.append([])
    one = []
    for i in range(len(data)):
        item = data[i]
        sort_data += item['lotteryDrawNum'] + "," + str.replace(item['lotteryDrawResult'],  " ",  ",") + "\n"
        unsort_data += item['lotteryDrawNum'] + "," + str.replace(item['lotteryUnsortDrawresult'],  " ",  ",") + "\n"
        if m <= i < len(data) - m and i % st == 0:
            sort_data_before_item, sort_data_after_item = get_count(data[i-m:i])
            one.append(sort_data_before_item["03"])
            for i0 in range(len(before)):
                sort_data_before[i0].append(sort_data_before_item[before[i0]])
            for i1 in range(len(after)):
                sort_data_after[i1].append(sort_data_after_item[after[i1]])

    ma = _ma(sort_data_before[2], 15)
    print(sort_data_before)
    print(sort_data_after)


    dot_count = 200
    plt.figure(figsize=((dot_count / 80) * 13, 8))
    # plt.plot(up[-dot_count:], linestyle="-", color="#999999", linewidth=2)
    # plt.plot(dn[-dot_count:], linestyle="-", color="#999999", linewidth=2)
    # plt.plot(ma[-dot_count:], linestyle="-", color="#F7A000", linewidth=2)
    # plt.plot(close_prices[-dot_count:], linestyle="-", color="#F52D2D", linewidth=4)
    plt.plot(sort_data_before[2], linestyle="-", color="#111111", linewidth=4)
    # plt.plot(sort_data_before[2], linestyle="-", color="#666666", linewidth=4)
    # plt.plot(sort_data_before[3], linestyle="-", color="#aaaaaa", linewidth=4)
    plt.plot(ma, linestyle="-", color="#F52D2D", linewidth=4)
    plt.show()
    exit()
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/sort_data.csv"
    with open(file_path,  "w",  encoding="utf8") as fp:
        fp.write(sort_data)
        fp.close()

    file_path = os.path.dirname(os.path.realpath(__file__)) + "/unsort_data.csv"
    with open(file_path,  "w",  encoding="utf8") as fp:
        fp.write(unsort_data)
        fp.close()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
