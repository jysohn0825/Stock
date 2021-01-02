from eunjeon import Mecab
import requests
from bs4 import BeautifulSoup
import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime, timedelta
TODAY = datetime.today().strftime("%Y-%m-%d")
YESTERDAY = (datetime.strptime(TODAY, '%Y-%m-%d') + timedelta(days=-1)).strftime("%Y-%m-%d")
LAST_TIME = (datetime.today() - timedelta(180)).strftime("%Y-%m-%d")
import csv

dicList = pd.read_csv("../crawling/dictionary.csv", usecols=[1,2], encoding="CP949")
dic = {}
for d in dicList.values:
    dic[d[0]] = d[1]

def stockData():
    sample = pd.read_csv("./Total.csv", usecols=[0,1], encoding='cp949')
    for i in sample.values:
        name = i[0]
        code = str(i[1])
        code = "0" * (6 - len(code)) + code
        if name != '게임테마' and name != '겨울테마' and name != '자율주행차테마' and name != '항공여행테마' and name != '인공지능테마':
            df = fdr.DataReader(code, LAST_TIME, TODAY)
            df['5Days'] = df['Close'].rolling(5).mean()
            df['10Days'] = df['Close'].rolling(10).mean()
            df['20Days'] = df['Close'].rolling(20).mean()
            df['60Days'] = df['Close'].rolling(60).mean()
            df['120Days'] = df['Close'].rolling(120).mean()
            df['emotion'] = 0
            df['count'] = 0
            df = df.reset_index()
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
                        if date[0] >= YESTERDAY:
                            news = i.find("dl").find("dd", {"class": "date"}).find_all("span")[0].text
                            if news != "인포스탁" and (date[1] < "09:00" or date[1] > "15:30"):
                                link = "http://www.paxnet.co.kr" + i.find("dl").find("dt").find("a")["href"]
                                subRequest = requests.get(link)
                                subSoup = BeautifulSoup(subRequest.text, "lxml")
                                div = subSoup.find("div", {"id": "contents"}).find("div", {"class": "cont-area"}).find(
                                    "div", {
                                        "class": "report-view"}).find("div", {"class": "report-view-cont"})
                                p = div.find_all("p")
                                content = div.find("div", {"id": "span_article_content"})
                                textSum = []
                                for cont in p:
                                    textSum.append(cont.text)
                                textTemp = "".join(textSum).join(content.text)
                                dateT = datetime.strptime(date[0], "%Y.%m.%d")

                                if date[1] > "15:30":
                                    dateT += timedelta(days=1)
                                    tempDateT = str(dateT).split(" ")
                                    emoDate = tempDateT[0].replace(".", "-")
                                    if emoDate == YESTERDAY:
                                        find_emo[emoDate] = find_emo.get(emoDate, "") + textTemp
                                        df.loc[df["Date"] == emoDate, "count"] += 1
                                elif date[1] < "09:00":
                                    emoDate = date[0].replace(".", "-")
                                    if emoDate == TODAY:
                                        find_emo[emoDate] = find_emo.get(emoDate, "") + textTemp
                                        df.loc[df["Date"] == emoDate, "count"] += 1
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
                    for sc in df.values:
                        if str(sc[0]) == k:
                            temp = int((score / count) * 100)
                            emotion = 0
                            if temp > 58:
                                emotion = 1
                            elif temp <= 46:
                                emotion = -1
                            df.loc[df["Date"] == k, "emotion"] = emotion

            df = df.dropna()
            df.reset_index(drop=False, inplace=True)
            df = df.iloc[-1]
            df1 = [str(df[1])[:10]]
            for j in range(2,len(df)) :
                df1.append(df[j])
            fs = open(f'./temp/{name}.csv', 'a', newline='', encoding='UTF-8-sig')
            wr = csv.writer(fs)
            wr.writerow(df1)
            fs.close()
        print(name,"Done")

stockData()