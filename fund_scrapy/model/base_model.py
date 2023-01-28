from fund_scrapy.common import mysql
from fund_scrapy.config import config


class BaseModel(mysql.Mysql):

    table = ""
    database = "data_center"

    def __init__(self, database: str = "data_center", table: str = ""):
        self.table = table
        self.database = database
        if database in config.Config().db_config.keys():
            db_config = config.Config().db_config[database]
            super().__init__(db_config)
        else:
            raise Exception("'" + database + "' is not find in db config from config.json!")

    def add(self, data=None):
        if data is None:
            data = {}
        if data == {}:
            return False

        keys = []
        values = []
        for key in data.keys():
            keys.append(str(key))
        for value in data.values():
            values.append(str(value if value is not None else ""))

        sql_key = "('" + "','".join(keys) + "')"
        sql_value = "('" + "','".join(values) + "')"

        sql = "INSERT INTO " + str(self.database) + "." + str(self.table) + " " + str(sql_key) + " VALUES " + str(sql_value)

        result = super().exec(sql)
        return result

    def add_all(self, data=None):

        if data is None:
            data = []
        if not data:
            return False

        sql_list = []
        for item in data:
            keys = []
            values = []
            updates = []
            for key in item.keys():
                keys.append(str(key))
                updates.append(key + "='" + str((item[key] if not (item[key] == "None" or item[key] is None) else "")) + "'")
            for value in item.values():
                values.append(str((value if not (value == "None" or value is None) else "")))

            sql_key = "(" + ",".join(keys) + ")"
            sql_value = "('" + "','".join(values) + "')"
            sql_item = "INSERT INTO " + str(self.database) + "." + str(self.table) + " " + str(sql_key) + " VALUES " \
                       + str(sql_value) + "ON DUPLICATE KEY UPDATE " + ", ".join(updates) + ";"
            sql_list.append(sql_item)

        result = super().exec_all(sql_list)
        return result

    @staticmethod
    def get(self, where="", fields: str = "*"):

        if where is None:
            where = ""
        if not where:
            return False

        sql = "SELECT " + fields + " FROM " + self.database + "." + self.table + " LIMIT 1"

        result = super().get_one(sql)
        return result
