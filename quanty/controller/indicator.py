from quanty import Cache
from quanty.service.indicator import IndicatorService
from quanty.service.stock import StockService
from quanty import keys


# 获取指标
class IndicatorController(object):

    # MACD指标
    def MACD(self, symbol: str = ""):
        cache = Cache()
        indicator = IndicatorService()
        if symbol != "":
            stocks = StockService().get_stocks()
        else:
            start_id = cache.read(keys.QUANTY_MACD)
            stocks = StockService().get_stocks(start_id=start_id, page_size=10)

        for stock in stocks:
            try:
                indicator.get_macd(stock["symbol"])
            except Exception as e:
                print(e)

        cache.set(keys.QUANTY_MACD, stocks[-1]["id"])
        return

    # 星辰线
    def YSTL(self, symbol: str = ""):
        cache = Cache()
        indicator = IndicatorService()
        if symbol != "":
            stocks = StockService().get_stocks(symbol=symbol)
        else:
            start_id = cache.read(keys.QUANTY_YSTL)
            stocks = StockService().get_stocks(start_id=start_id, page_size=10)

        for stock in stocks:
            try:
                indicator.get_ystl(stock["symbol"])
            except Exception as e:
                print(e)

        cache.set(keys.QUANTY_YSTL, stocks[-1]["id"])
