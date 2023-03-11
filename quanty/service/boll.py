import os
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as m_date


def _ma(close_prices, n):
    close_prices = np.array(close_prices)
    ma = []
    for index in range(1, len(close_prices)):
        start = index - n if index - n >= 0 else 0
        count = index - start
        ma.append(np.average(close_prices[start:index]))
    return ma


def _md(close_prices, n):
    close_prices = np.array(close_prices)
    md = []
    for index in range(1, len(close_prices)):
        start = index - n if index - n >= 0 else 0
        count = index - start
        md.append(np.std(close_prices[start:index]))
    return md


if __name__ == "__main__":
    print("running. pid: " + str(os.getpid()))

    n = 30  # 窗口大小
    k = 2  # 参数
    data = {}
    code = "SH600570"
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/../data/nav/" + str(code) + ".json"
    try:
        with open(file_path, "r", encoding="utf8") as fp:
            data = json.load(fp)
            fp.close()
    except Exception as e:
        print(e)
        exit()

    close_prices = list(map(lambda x: x["close"], data))
    price_time = list(map(lambda x: x["timestamp"], data))
    price_time = np.array(price_time)
    ma = np.array(_ma(close_prices, n))
    md = np.array(_md(close_prices, n))
    up = ma + 2 * md
    dn = ma - 2 * md

    file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/indicator"
    try:
        boll = np.array(list(zip(price_time, ma, close_prices, up, dn)))
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(file_path + "/" + str(code) + ".json", "a+", encoding="utf8") as fp:
            fp.write(json.dumps(boll.tolist()))
            fp.close()
    except Exception as e:
        print(e)

    # dot_count = 200
    # plt.figure(figsize=((dot_count / 80) * 13, 8))
    # plt.plot(up[-dot_count:], linestyle="-", color="#999999", linewidth=2)
    # plt.plot(dn[-dot_count:], linestyle="-", color="#999999", linewidth=2)
    # plt.plot(ma[-dot_count:], linestyle="-", color="#F7A000", linewidth=2)
    # plt.plot(close_prices[-dot_count:], linestyle="-", color="#F52D2D", linewidth=4)
    # plt.plot(md[-dot_count:], linestyle="-", color="#F52D2D", linewidth=4)
    # plt.show()
    pass
