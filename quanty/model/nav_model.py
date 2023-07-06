from quanty.model import BaseModel


class NavModel(BaseModel):

    table = "xueqiu_nav"
    database = "data_center"
    
    def __init__(self):
        super().__init__(table=self.table, database=self.database)
