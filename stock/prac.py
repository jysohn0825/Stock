from eunjeon import Mecab
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

dicList = pd.read_csv("../crawling/dictionary.csv", usecols=[1,2], encoding="CP949")
dic = {}
for d in dicList.values:
    dic[d[0]] = d[1]

stock = pd.read_csv("./Total.csv", usecols = [0,1,2], encoding="CP949")

count = 0
sum = 0
avg = 0

for s in stock.values:
    stock_code = pd.read_csv(f"./stockList/{s[0]}.csv", encoding="UTF-8")
    for sc in stock_code.values:
        if sc[15] != 0:
            sum += sc[15]
            count += 1
if count != 0:
    avg = int(sum/count)
