from quanty.model.nav_model import NavModel

class BuySignal(object):
    def __init__(self):
        where = ""

        nav = NavModel().\
            where("").\
            fields("*").\
            limit(10000).\
            all()
        pass
