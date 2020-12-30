import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import strptime, sleep

df = pd.DataFrame(index=range(0,), columns=["code", "date", "count", "emotion"])
count = 0
stock = pd.read_csv("code.csv", usecols=[1], encoding="UTF-8")
file = open("../stock/word.txt", "a", encoding="UTF-8")
for s in stock.values:
    code = str(s[0])
    code = "0" * (6-len(code)) + code
    page = 1
    flag = False
    dic = {}
    while True:
        request = requests.get(f"http://www.paxnet.co.kr/tbbs/list?tbbsType=L&id={code}&page={page}")
        soup = BeautifulSoup(request.text, "lxml")
        ul = soup.find("ul", {"id": "comm-list"})
        li = ul.find_all("li")
        for l in li[1:]:

            # + 게시글 내용도 크롤링 (discuss_content.py)
            # 크롤링한 내용을 토대로 감정분석
            # 날짜별 게시글의 수 및 긍부정 판독을 하면 LSTM을 위한 값이 나올 것
            link = l.find("div",{"class":"type type_"})["data-seq"]
            subRequest = requests.get(f"http://www.paxnet.co.kr/tbbs/view?id={code}&seq={link}")
            subSoup = BeautifulSoup(subRequest.text, "lxml")
            p = subSoup.find("div", {"id":"bbsWrtCntn"}).find_all("p")
            for t in p:
                file.write(t.text)
            title = l.find("a", {"class":"best-title"})
            file.write(title.text)
            print(code, page, title.text)
            date = str(l.find("div", {"class": "date"}).find("span")["data-date-format"])
            temp = date.split(" ")
            # 2020년 게시글이 아닐 경우 flag 변경 및 break
            if temp[5] != "2020":
                flag = True
                break
            else:
                # Dec 등 영어로 표시된 월을 숫자로 변경
                month = str(strptime(temp[1], '%b').tm_mon)
                # 다른 csv 파일과 포맷을 맞추기 위해 1을 01로 변경
                key = f"2020-{'0' * (2 - len(month)) + month}-{temp[2]}"
                # 날짜별 게시글이 있을 경우 +1 아닐 경우 1
                if key in dic:
                    dic[key] += 1
                else:
                    dic[key] = 1
                pass
        # flag 체크 후 페이지 변경 or 반복문 탈출
        if flag:
            break
        else:
            page += 1
        sleep(1)
    # 종목코드에 해당하는 날짜별 게시글 개수 추가
    # for key, value in dic.items():
    #     df.loc[count] = (code, key, value)
    #     count += 1
# csv에 넣기
# df.to_csv("paxnet.csv")

print("완료")