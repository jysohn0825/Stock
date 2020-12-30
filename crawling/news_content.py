import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import strptime, sleep

file = open("word.txt", "a", encoding="UTF-8")

thema = ["항공여행"]#,"지능형로봇_인공지능(AI)"]

for name in thema:
    df = pd.read_csv(f"{name}.csv", usecols=[1], encoding="CP949")
    file = open(f"{name}.txt", "w", encoding="UTF-8")
    for i in df.values:
        code = str(i[0])
        code = "0" * (6 - len(code)) + code
        flag = False
        page = 1
        while True:
            request = requests.get(f"http://www.paxnet.co.kr/news/{code}/stock?currentPageNo={page}")
            soup = BeautifulSoup(request.text, "lxml")
            ul = soup.find("div", {"id":"contents"}).find("div", {"class":"board-thumbnail"}).find("ul", {"class":"thumb-list"})
            li = ul.find_all("li")
            sleep(10)
            for i in li:
                date = i.find("dl").find("dd", {"class": "date"}).find_all("span")[1].text
                if date > "2020.06.21":
                    news = i.find("dl").find("dd", {"class": "date"}).find_all("span")[0].text
                    if news != "인포스탁":
                        link = "http://www.paxnet.co.kr" + i.find("dl").find("dt").find("a")["href"]
                        subRequest = requests.get(link)
                        subSoup = BeautifulSoup(subRequest.text, "lxml")
                        div = subSoup.find("div",{"id":"contents"}).find("div",{"class":"cont-area"}).find("div",{"class":"report-view"}).find("div",{"class":"report-view-cont"})
                        p = div.find_all("p")
                        for cont in p:
                            file.write(cont.text)
                        sleep(10)
                else:
                    flag = True
                    break
            print(name,code,page)
            page += 1
            if flag:
                break
