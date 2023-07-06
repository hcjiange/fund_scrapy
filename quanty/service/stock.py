from quanty.model.stock_model import StockModel
from quanty.model.nav_model import NavModel


class StockService(object):

    def get_stocks(self, symbol: str = "", start_id: int = 0, page: int = 1, page_size: int = 20):
        where = {}
        if symbol != "":
            where["symbol"] = symbol
        if start_id != 0 and start_id != "":
            where["id"] = [">", start_id]

        return StockModel().where(where).page(page, page_size).all()

    def get_nav(self, code: str):
        return NavModel().where({"code": code}).order().all()
