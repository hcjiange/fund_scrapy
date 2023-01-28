from fund_scrapy.model import base_model


class StockModel(base_model.BaseModel):

    table = "xueqiu_stock"
    database = "data_center"
    
    def __init__(self):
        super().__init__(table=self.table, database=self.database)
