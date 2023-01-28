import scrapy
import requests
import json
from fund_scrapy.service.stock import Stock

from scrapy.http.cookies import CookieJar


class StockSpider(scrapy.Spider):

    name = "sync_stocks"
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
        self.get_stocks(response)
        return

    def get_stocks(self, response):

        url = "https://stock.xueqiu.com/v5/stock/screener/quote/list.json"

        self.page = self.page + 1
        if self.page > 20:
            return

        params_type = "sh_sz"
        params = {
            'page': self.page,
            'size': self.page_size,
            'order': "desc",
            'orderby': "current_year_percent",
            'order_by': "current_year_percent",
            'market': "CN",
            'type': params_type,
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
            if "list" in res['data'].keys():
                data = res['data']['list']
        if data is not None and len(data) > 0:
            Stock().save_stocks(data)
            self.get_stocks(response)
        return data
