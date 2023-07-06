from exec.quanty import IndicatorController
import sys
import os

if __name__ == '__main__':
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(root_path)
    IndicatorController().YSTL("SH601360")
    pass
