import sys
import os
from scrapy.cmdline import execute

if __name__ == '__main__':
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(root_path)
    execute(['scrapy', 'crawl', 'sync_history_nav'])
