import scrapy
import requests
import json
import os
import datetime
import hashlib
from fund_scrapy.service.stock import Stock

from scrapy.http.cookies import CookieJar


class StockSpider(scrapy.Spider):

    name = "sync_history_nev"
    start_urls = ["https://xueqiu.com/hq"]
    page = 0
    page_size = 500

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'origin': "https://xueqiu.com",
            'referer': "https://xueqiu.com/hq",
            'cookie': "",
        },
    }  # 添加的请求头
    cookies = []

    def parse(self, response, **kwargs):

        cookie_jar = CookieJar()
        cookie_jar.extract_cookies(response, response.request)
        cookies = dict()
        cookies_str = ""
        for k, v in cookie_jar._cookies.items():
            for i, j in v.items():
                for m, n in j.items():
                    cookies[m] = n.value
                    cookies_str += str(m) + "=" + str(n.value) + "; "
        self.custom_settings["DEFAULT_REQUEST_HEADERS"]["cookie"] = cookies_str
        self.cookies = cookies
        self.get_history_nev(response)
        return

    def get_history_nev(self, response):

        url = "https://stock.xueqiu.com/v5/stock/chart/kline.json"

        self.page = self.page + 1
        if self.page > 20:
            return
        symbol = "SH600601"

        params = {
            'symbol': symbol,
            'begin': 1674268101153,
            'period': "day",
            'type': "before",
            'count': "-300",
            'market': "CN",
            'indicator': "kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance",
        }

        req = requests.get(url=url, params=params, headers=self.custom_settings["DEFAULT_REQUEST_HEADERS"])

        req.content.decode("utf-8")
        if req.status_code == 400:
            return

        response = req.text
        req.close()
        res = json.loads(response)
        data = None
        if "data" in res.keys():
            if "item" in res['data'].keys():
                data = res['data']['item']

        history_nev = []
        if data is not None and len(data) > 0:
            for item in data:
                history_nev.append({
                    'timestamp': item[0],
                    'volume': item[1],
                    'open': item[2],
                    'high': item[3],
                    'low': item[4],
                    'close': item[5],
                    'chg': item[6],
                    'percent': item[7],
                    'turnoverrate': item[8],
                    'amount': item[9],
                    'volume_post': item[10],
                    'amount_post': item[11],
                    'pe': item[12],
                    'pb': item[13],
                    'ps': item[14],
                    'pcf': item[15],
                    'market_capital': item[16]
                })

            sub_dir = hashlib.md5(symbol[2:].encode('utf8')).hexdigest()[-2:]
            cache_path = os.path.dirname(os.path.realpath(__file__)) + "/../data/history/" + sub_dir
            if not os.path.exists(cache_path):
                os.makedirs(cache_path)
            try:
                with open(cache_path + "/" + symbol + ".json", "w+", encoding="utf8") as fp:
                    fp.write(json.dumps(history_nev) + '\n')
            except Exception as e:
                print(e)

        return
