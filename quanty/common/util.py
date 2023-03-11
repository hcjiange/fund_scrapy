import time


# 时间戳转日期
def time_format(data: list):
    for index in range(len(data)):
        data[index] = time.strftime("%Y-%m-%d", time.localtime((int(data[index][:13]) / 1000)))
        pass
    return data
