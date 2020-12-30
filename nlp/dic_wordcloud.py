from eunjeon import Mecab
import pandas as pd

dicList = pd.read_csv("../crawling/dictionary.csv", usecols=[1,2], encoding="CP949")
dic = []
for d in dicList.values:
    dic.append(d[0])
wordCount = {}
thema = ["게임","겨울","자율주행차","항공여행"]
for t in thema:
    m = Mecab()
    file = open(f"../crawling/{t}.txt", encoding="UTF-8")
    list = m.morphs(file.readline())
    for word in list:
        if word in dic:
            wordCount[word] = wordCount.get(word, 0) + 1
from wordcloud import WordCloud
wc = WordCloud(font_path="C:\\Windows\\Fonts\\gulim.ttc",
               background_color="white",width=1000,height=1000,max_words=358,max_font_size=300)
wc.generate_from_frequencies(wordCount)
wc.to_file("wcPic.png")




