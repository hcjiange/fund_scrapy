from quanty.model import BaseModel


class StockModel(BaseModel):

    table = "xueqiu_stock"
    database = "data_center"
    
    def __init__(self):
        super().__init__(table=self.table, database=self.database)
