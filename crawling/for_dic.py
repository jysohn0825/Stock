from eunjeon import Mecab
import pandas as pd


thema = ["게임","겨울","자율주행차","항공여행"]
file = open("total_word.txt", "a", encoding="UTF-8")
list = []
for t in thema:
    sample = pd.read_csv(f"{t}_count.csv", usecols=[1], encoding="UTF-8")
    for i in sample.values:
        if i not in list:
            file.write(i[0]+"\n")
            list.append(i[0])
