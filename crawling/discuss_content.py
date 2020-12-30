import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import strptime

df = pd.DataFrame(index=range(0,), columns=["code", "date", "count"])
count = 0
stock = pd.read_csv("code.csv", usecols=[1], encoding="CP949")

request = requests.get(f"http://www.paxnet.co.kr/tbbs/list?tbbsType=L&id=005930&page=1")
soup = BeautifulSoup(request.text, "lxml")
ul = soup.find("ul", {"id": "comm-list"})
li = ul.find_all("li")
for l in li[1:2]:
    link = l.find("div",{"class":"type type_"})["data-seq"]
    subRequest = requests.get(f"http://www.paxnet.co.kr/tbbs/view?id=005930&seq={link}")
    subSoup = BeautifulSoup(subRequest.text, "lxml")
    span = subSoup.find("div", {"id":"bbsWrtCntn"}).find_all("p")
    for s in span:
        print(s.text, end = " ")