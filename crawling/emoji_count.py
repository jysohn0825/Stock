from eunjeon import Mecab
import pandas as pd

dicList = pd.read_csv("dictionary.csv", usecols=[1], encoding="CP949")
dic = []

for d in dicList.values:
    dic.append(d[0])

wordCount = {}
thema = ["게임","겨울","자율주행차","항공여행"]
for t in thema:
    m = Mecab()
    file = open(f"{t}.txt", encoding="UTF-8")
    list = m.morphs(file.readline())
    for word in list:
        if word in dic:
            wordCount[word] = wordCount.get(word, 0) + 1
