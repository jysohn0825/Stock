from eunjeon import Mecab
import pandas as pd

thema = ["게임","겨울","자율주행차","항공여행"]
for t in thema:
    m = Mecab()
    file = open(f"{t}.txt", encoding="UTF-8")
    list = m.morphs(file.readline())
    wordCount = {}
    for word in list:
        wordCount[word] = wordCount.get(word, 0) + 1

    sorted(wordCount.items(), key=lambda x: x[1], reverse=True)

    word_list = sorted(wordCount.items(), key=lambda x: x[1], reverse=True)

    df = pd.DataFrame(index=range(0,), columns=["word", "count"])
    count = 0
    for wl in word_list[:3000]:
        df.loc[count] = (wl[0],wl[1])
        count+=1
    df.to_csv(f"{t}_count.csv")