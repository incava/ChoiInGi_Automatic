import sys
from coupang import Pasing

url = "https://www.coupang.com"
search_name = "아이패드"
filter_name = ["프로"]
auto = Pasing(url, search_name, 1000000, sys.maxsize, filter_name)
auto.auto_start()


