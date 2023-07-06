import time

import numpy as np


# 时间戳转日期
def time_format(data: list):
    for index in range(len(data)):
        data[index] = time.strftime("%Y-%m-%d", time.localtime((int(data[index][:13]) / 1000)))
        pass
    return data


# 合并多个n二位数字为n+1维数组
def merger_lists(lists: list):
    data = []
    for index in range(len(lists[0])):
        item = []
        for n in range(len(lists)):
            item.append(lists[n][index])
        data.append(item)
    return data
