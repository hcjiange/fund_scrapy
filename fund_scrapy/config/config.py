import json
import os


class Config(object):
    db_config = {}

    def __init__(self):
        config = self.get_cache()
        if "db" in config.keys():
            self.db_config = config['db']
        else:
            raise Exception("'db' is not find in config.json!")

    @staticmethod
    def get_cache():
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + "/" + "config.json", "r", encoding="utf8") as fp:
                json_data = json.load(fp)
                fp.close()
                return json_data
        except Exception as e:
            print(e)
