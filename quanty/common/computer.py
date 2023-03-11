import numpy as np


# n日数据
def REF(data: list, n: int):
    ref = []
    for index in range(n):
        ref.append(False)
    ref_data = data[:-n]
    ref.extend(ref_data)
    return ref


# n日最大
def HHV(data: list, n: int):
    hhv = []
    for index in range(1, len(data)):
        start_i = index - n
        if start_i < 0:
            start_i = 0
        hhv.append(max(data[start_i:index]))
    return hhv


# n日最小
def LLV(data: list, n: int):
    hhv = []
    for index in range(1, len(data)):
        start_i = index - n
        if start_i < 0:
            start_i = 0
        hhv.append(min(data[start_i:index]))
    return hhv


# n日均值
def MA(data: list, n: int):
    data = np.array(data)
    ma = []
    for index in range(1, len(data)):
        start_i = index - n
        if start_i < 0:
            start_i = 0
        ma.append(np.average(data[start_i:index]))
    return ma
