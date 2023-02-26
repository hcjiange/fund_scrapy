from fund_scrapy.model.stock_model import StockModel
from fund_scrapy.model.nav_model import NavModel


class Stock(object):

    @staticmethod
    def save_stocks(stocks):

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

        stock_obj = StockModel()
        res = stock_obj.save_all(new_stocks)
        return

    @staticmethod
    def save_history_nav(history_nav):

        for nav in history_nav:
            for key in nav:
                if nav[key] is None:
                    nav[key] = 0
        nav_obj = NavModel()
        res = nav_obj.save_all(history_nav)
        return

    @staticmethod
    def get_stocks(where, page, page_size):
        stock_model = StockModel()
        stocks = stock_model.where(where).page(page, page_size).all()
        print(stock_model.get_last_sql())
        return stocks
