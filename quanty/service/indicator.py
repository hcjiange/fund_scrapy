import matplotlib.pyplot as plt
import numpy as np
from quanty.model.nav_model import NavModel
from quanty.common import computer
from quanty.common import util
from quanty import File
import json
import datetime


class IndicatorService(object):

    def __init__(self):
        pass

    # MACD
    def get_macd(self, symbol: str):

        code = symbol[2:]
        nav_data = NavModel().where({"code": code}).order_asc("price_time").fields("close").all()

        if nav_data is None:
            return

        nav = list(map(lambda x: x["close"], nav_data))

        if len(nav) < 3:
            return

        last_ema12 = nav[0] + (nav[1] - nav[0]) * 2/13
        last_ema26 = nav[0] + (nav[1] - nav[0]) * 2/27
        diff = last_ema12 - last_ema26
        last_dea = nav[0] + diff * 2/10
        bar = 2 * (diff - last_dea)

        data_diff = []
        data_dea = []
        data_bar = []
        for current_price in nav[2:]:
            ema12 = self.__ema(12, last_ema12, current_price)
            ema26 = self.__ema(26, last_ema26, current_price)
            diff = ema12 - ema26
            dea = self.__ema(9, last_dea, diff)
            bar = 2 * (diff - dea)

            data_diff.append(diff)
            data_dea.append(dea)
            data_bar.append(bar)
            last_ema12 = ema12
            last_ema26 = ema26
            last_dea = dea

        count = 72

        # plt.figure(figsize=(15, 2))
        # plt.plot(data_diff[-count:], linestyle="-", color="#999999", linewidth=2)
        # plt.plot(data_dea[-count:], linestyle="-", color="#F7A000", linewidth=2)
        # # plt.bar(range(1, len(data_bar)), data_bar)
        # plt.plot(data_bar[-count:], linestyle="-", color="#F52D2D", linewidth=1)
        # plt.show()

        return

    def __ema(self, n, last_ema, current_price):
        return (2 * current_price + (n - 1) * last_ema)/(n + 1)

    # EMV
    def get_emv(self, data):
        return

    # BOLL
    def get_boll(self, nav):
        n = 20
        return

    def get_ystl(self, symbol: str):

        code = symbol[2:]
        nav_data = NavModel().where({"code": code}).order_asc("price_time").fields("close,open,low,high,price_time").all()
        if nav_data is None:
            return

        close = np.array(list(map(lambda x: x["close"], nav_data)))
        open = np.array(list(map(lambda x: x["open"], nav_data)))
        low = np.array(list(map(lambda x: x["low"], nav_data)))
        high = np.array(list(map(lambda x: x["high"], nav_data)))
        price_time = np.array(list(map(lambda x: x["price_time"], nav_data)))
        price_time = util.time_format(price_time)

        if len(close) < 3:
            return

        jrh = computer.HHV(close, 2)
        jrl = computer.LLV(close, 2)
        ma3 = computer.MA(close, 3)
        ystl = (close * 3 + low + open + high) / 6
        #
        # count = 62
        # plt.figure(figsize=(15, 6))
        # plt.plot(ystl[-count:], linestyle="-", color="#999999", linewidth=2)
        # plt.plot(ma3[-count:], linestyle="-", color="#F7A000", linewidth=2)
        # plt.plot(llv[-count:], linestyle="-", color="#F52D2D", linewidth=1)
        # plt.plot(hhv[-count:], linestyle="-", color="#F52D2D", linewidth=1)
        # plt.show()
        #
        # plt.figure(figsize=(15, 6))
        # plt.plot(close[-count:], linestyle="-", color="#F52D2D", linewidth=2)
        # plt.show()

        var1 = ((close > computer.REF(close,1)) * (close > computer.REF(close,2)))
        var = []
        var.append(var1)
        for index in range(0, 8):
            if index % 2 == 0:
                var.append((computer.REF(var[index], 1) * (close >= computer.REF(close, 1)) * (close <= computer.REF(close, 2))))
            else:
                var.append((computer.REF(var[index], 1) * (close <= computer.REF(close, 1)) * (close >= computer.REF(close, 2))))
        varA = (computer.REF(var[8], 1) * (close >= computer.REF(close, 1)) * (close <= computer.REF(close, 2)))
        varB = (computer.REF(varA, 1) * (close <= computer.REF(close, 1)) * (close >= computer.REF(close, 2)))
        varC = (computer.REF(varB, 1) * (close >= computer.REF(close, 1)) * (close <= computer.REF(close, 2)))
        varD = (close < computer.REF(close, 1)) * (close < computer.REF(close, 2))
        varE = (computer.REF(varD, 1)) * (close >= computer.REF(close, 1)) * (close <= computer.REF(close, 2))
        varF = (computer.REF(varE, 1)) * (close <= computer.REF(close, 1)) * (close >= computer.REF(close, 2))
        var10 = (computer.REF(varF, 1)) * (close >= computer.REF(close, 1)) * (close <= computer.REF(close, 2))
        var.append(var10)
        for index in range(9, 18):
            if index % 2 == 0:
                var.append((computer.REF(var[index], 1) * (close >= computer.REF(close, 1)) * (close <= computer.REF(close, 2))))
            else:
                var.append((computer.REF(var[index], 1) * (close <= computer.REF(close, 1)) * (close >= computer.REF(close, 2))))

        var19_data = varD + varE + varF
        for index in range(9, 19):
            var19_data += var[index]
        var.append((computer.REF(var19_data, 1)) * var1)

        var1A_data = varA + varB + varC
        for index in range(0, 10):
            var1A_data += var[index]
        var1A = (computer.REF(var1A_data, 1) * varD)

        # 红色持股
        keeping = var1A_data
        # 离场
        leave = [];
        for index in range(len(keeping)):
            if keeping[index]:
                leave.append(jrl[index])
            else:
                leave.append(0)
        tomorrow_leave = leave
        today_leave = computer.REF(leave, 1)
        
        # 观望
        looking = var19_data
        # 进场
        go_in = []
        for index in range(len(looking)):
            if looking[index]:
                go_in.append(jrh[index])
            else:
                go_in.append(0)
        tomorrow_in = go_in
        today_in = computer.REF(go_in, 1)

        # 短买
        short_by = var[-1]
        short_leave = var1A
        # 急速超跌
        quick_down = (close - computer.MA(close, 34))/computer.MA(close, 34) * 100 < -14

        # 星辰线
        star_line = 20 * ystl
        for index in range(1, 19):
            star_line = star_line + ((20 - index) * computer.REF(ystl, index))
        star_line = (star_line + computer.REF(ystl, 20))/211
        # 牵牛线
        ma26 = computer.MA(close, 26)

        # 等待
        wait = []
        for index in range(0, len(star_line)):
            if ma3[index] > star_line[index]:
                wait.append(star_line[index])
            else:
                wait.append(ma3)


        data = util.merger_lists([short_by, close, price_time, today_in, today_leave, tomorrow_in, tomorrow_leave])
        # print(np.array(list(zip(short_by, close, price_time))).tolist())
        # File().write_file(symbol, "indicator/ystl/short_by", json.dumps(np.array(list(zip(short_by, close, price_time))).tolist()))
        File().write_file(symbol, "indicator/ystl/short_by", json.dumps(np.array(data).tolist()))



        exit()
