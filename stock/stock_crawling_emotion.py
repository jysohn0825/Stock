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

for s in stock.values[10:11]:
    stock_code = pd.read_csv(f"./stockList/{s[0]}.csv", encoding="UTF-8")
    stock_code["emotion"] = 0
    stock_code["count"] = 0
    code = str(stock_code["종목코드"][1])
    code = "0" * (6-len(code)) + code
    if code != "123456" and code != "234567" and code != "345678" and code != "456789" and code != "567890":
        flag = False
        page = 1
        find_emo = {}
        while True:
            request = requests.get(f"http://www.paxnet.co.kr/news/{code}/stock?currentPageNo={page}")
            soup = BeautifulSoup(request.text, "lxml")
            ul = soup.find("div", {"id": "contents"})
            div1 = ul.find("div", {"class": "board-thumbnail"})
            if div1 != None:
                div2 = div1.find("ul", {"class": "thumb-list"})
                li = div2.find_all("li")
                for i in li:
                    date = i.find("dl").find("dd", {"class": "date"}).find_all("span")[1].text.split(" ")
                    if date[0] >= "2017.01.01":
                        news = i.find("dl").find("dd", {"class": "date"}).find_all("span")[0].text
                        if news != "인포스탁" and (date[1] < "09:00" or date[1] > "15:30"):
                            link = "http://www.paxnet.co.kr" + i.find("dl").find("dt").find("a")["href"]
                            subRequest = requests.get(link)
                            subSoup = BeautifulSoup(subRequest.text, "lxml")
                            div = subSoup.find("div", {"id": "contents"}).find("div", {"class": "cont-area"}).find("div", {
                                "class": "report-view"}).find("div", {"class": "report-view-cont"})
                            p = div.find_all("p")
                            content = div.find("div", {"id": "span_article_content"})
                            textSum = []
                            for cont in p:
                                textSum.append(cont.text)
                            textTemp = "".join(textSum)
                            textTemp = "".join(content.text)
                            dateT = datetime.strptime(date[0], "%Y.%m.%d")

                            if date[1] > "15:30":
                                dateT += timedelta(days=1)
                                tempDateT = str(dateT).split(" ")
                                emoDate = tempDateT[0].replace(".", "-")
                                find_emo[emoDate] = find_emo.get(emoDate, "") + textTemp
                                stock_code.loc[stock_code["Date"] == emoDate, "count"] += 1
                            elif date[1] < "09:00":
                                emoDate = date[0].replace(".", "-")
                                find_emo[emoDate] = find_emo.get(emoDate, "") + textTemp
                                stock_code.loc[stock_code["Date"] == emoDate, "count"] += 1
                    else:
                        flag = True
                        break
                page += 1
                if flag:
                    break
            else:
                break
        for k, v in find_emo.items():
            count, score = 0, 0
            m = Mecab()
            list = m.morphs(v)
            for word in list:
                if word in dic.keys():
                    if dic[word] == 1:
                        score += 1
                    count += 1
            if count != 0:
                for sc in stock_code.values:
                    if str(sc[0]) == k:
                        temp = int((score / count) * 100)
                        emotion = 0
                        if temp > 58:
                            emotion = 1
                        elif temp <= 46:
                            emotion = -1
                        stock_code.loc[stock_code["Date"] == k, "emotion"] = emotion
        stock_code.to_csv(f"./sList/{s[0]}.csv")
        print(s[0], "Done")

