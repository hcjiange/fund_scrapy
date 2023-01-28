
class IndicatorService(object):

    def __init__(self):
        pass

    # MACD
    def get_macd(self, nev):
        if nev is None:
            nev = []

        last_ema12 = nev[0] + (nev[1] - nev[0]) * 2/13
        last_ema26 = nev[0] + (nev[1] - nev[0]) * 2/27
        diff = last_ema12 - last_ema26
        last_dea = nev[0] + diff * 2/10
        bar = 2 * (diff - last_dea)

        data_diff = []
        data_dea = []
        data_bar = []
        for current_price in nev[2:]:
            # DIF£¨xn£© = EMA12£¨xn£© ¨C EMA26£¨xn£©£¬
            # DEA£¨xn£© = EMA9[DIF£¨xn£©]£¬
            # MACD£¨xn£© = [DIF£¨xn£© ¨C DEA£¨xn£©] x 2¡£
            ema12 = self.__ema(12, last_ema12, current_price)
            ema26 = self.__ema(26, last_ema26, current_price)
            diff = ema12 - ema26
            dea = self.__ema(9, last_dea, diff)
            bar = 2 * (diff - dea)

            data_diff.append(diff)
            data_dea.append(dea)
            data_bar.append(bar)
            last_ema12 = ema12
            last_ema26 = ema26
            last_dea = dea

        return {"data_diff": data_diff, "data_dea": data_dea, "data_bar": data_bar, "bar": bar}

    def __ema(self, n, last_ema, current_price):
        return (2 * current_price + (n - 1) * last_ema)/(n + 1)

    # EMV
    def get_emv(self, data):
        return
