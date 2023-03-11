import scrapy
import requests
import json
import datetime
import time
from fund_scrapy.spiders import Cache
from fund_scrapy.service.stock import Stock
from fund_scrapy.model.nav_model import NavModel

from scrapy.http.cookies import CookieJar

from fund_scrapy import keys


class StockSpider(scrapy.Spider):

    name = "sync_history_nav"
    start_urls = ["https://xueqiu.com/hq"]
    page = 0
    page_size = 100

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
        self.get_history_nav(response)
        return

    def get_history_nav(self, response):

        url = "https://stock.xueqiu.com/v5/stock/chart/kline.json"
        self.page = self.page + 1
        if self.page > 300:
            return

        cache_id = Cache().read(keys.SPIDER_NAV + str(datetime.datetime.now().strftime("%Y%m%d")))
        if cache_id is not None and cache_id != "":
            start_id = cache_id
        else:
            start_id = 0

        stocks = Stock().get_stocks({"id": [">", start_id]}, 1, self.page_size)
        if len(stocks) == 0:
            return
        for stock in stocks:

            symbol = stock["symbol"]
            code = symbol[2:]

            begin = NavModel().where({"code": code}).max("price_time")

            params = {
                'symbol': symbol,
                'begin': int((str(begin) if begin is not None and str(begin) != "" else '1675699538966')),
                'period': "day",
                'type': "before",
                'count': "-284",
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

            history_nav = []
            if data is not None and len(data) > 0:
                for item in data:
                    history_nav.append({
                        'code': code,
                        'price_time': item[0],
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
            Stock().save_history_nav(history_nav)
        last_data = stocks[(len(stocks) - 1)]
        Cache().set(keys.SPIDER_NAV + str(datetime.datetime.now().strftime("%Y%m%d")), last_data["id"])
        time.sleep(5)
        self.get_history_nav(None)
        return
