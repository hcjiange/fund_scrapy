import hashlib
import os
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as m_date
import numpy as np

from fund_scrapy.service.indicator import IndicatorService


class IndicatorController(object):

    def build_macd(self):

        symbol = "SH600601"
        sub_dir = hashlib.md5(symbol[2:].encode('utf8')).hexdigest()[-2:]
        history_path = os.path.dirname(os.path.realpath(__file__)) + "/../data/history/" + sub_dir

        try:
            with open(history_path + "/" + symbol + ".json", "r", encoding="utf8") as fp:
                history_data = json.load(fp)
                fp.close()
            history_nev = list(map(lambda x: x["close"], history_data))
            macd_data = IndicatorService().get_macd(history_nev)

            macd_path = os.path.dirname(os.path.realpath(__file__)) + "/../data/macd/" + sub_dir
            # if not os.path.exists(macd_path):
            #     os.makedirs(macd_path)
            # with open(macd_path + "/" + symbol + ".json", "a+", encoding="utf8") as fp:
            #     fp.write(json.dumps(macd_data) + "\n")
            #     fp.close()
            data_diff = np.array(macd_data["data_diff"][-72:])
            data_dea = np.array(macd_data["data_dea"][-72:])
            data_bar = np.array(macd_data["data_bar"][-72:])

            plt.figure(figsize=(15, 2))
            plt.plot(data_diff, linestyle="-", color="#999999", linewidth=2)
            plt.plot(data_dea, linestyle="-", color="#F7A000", linewidth=2)
            # plt.bar(range(1, len(data_bar)), data_bar)
            # plt.plot(data_bar, linestyle="-", color="#F52D2D", linewidth=1)
            plt.show()

        except Exception as e:
            print(e)

