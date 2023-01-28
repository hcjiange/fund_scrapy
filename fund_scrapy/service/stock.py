from fund_scrapy.model import stock_model
import os
import json


class Stock(object):

    def save_stocks(self, stocks):

        new_stocks = []
        for stock in stocks:
            for key in stock:
                if stock[key] is None:
                    stock[key] = 0

            new_stocks.append({
                'code': stock['symbol'][2:],
                'name': stock['name'],
                'symbol': stock['symbol'],
                'type': stock['type'],
                'percent': stock['percent'],
                'pb_ttm': stock['pb_ttm'],
                'float_shares': stock['float_shares'],
                'current': stock['current'],
                'amplitude': stock['amplitude'],
                'current_year_percent': stock['current_year_percent'],
                'float_market_capital': stock['float_market_capital'],
                'market_capital': stock['market_capital'],
                'dividend_yield': stock['dividend_yield'],
                'amount': stock['amount'],
                'chg': stock['chg'],
                'eps': stock['eps'],
                'volume': stock['volume'],
                'volume_ratio': stock['volume_ratio'],
                'turnover_rate': stock['turnover_rate'],
                'pe_ttm': stock['pe_ttm'],
                'total_shares': stock['total_shares'],
                'isvalid': 1,
            })

        stock_obj = stock_model.StockModel()
        res = stock_obj.add_all(new_stocks)
        return