import FinanceDataReader as fdr
import pandas as pd

df = pd.DataFrame(index=range(0, ), columns=["thema", "score", "change"])
count = 0
thema = ["게임","겨울","자율주행차","항공여행"]
for t in thema:
    for_code = pd.read_csv(f"../crawling/{t}.csv", usecols=[1], encoding="CP949")
    for i in for_code.values:
        if i[0] == "":
            break
        code = str(i[0])
        code = "0" * (6-len(code)) + code
        for_emo = pd.read_csv(f"./emoScore/{t}/{code}.csv", usecols=[2,3], encoding="CP949")
        find_change = fdr.DataReader(code, "2020-08-24").rename_axis("Date").reset_index().sort_values(by=["Date"], ascending=False)
        for fe in for_emo.values:
            emo_date = str(fe[0]).replace(".","-")
            for fc in find_change.values:
                change_date = str(fc[0]).split(" ")
                if change_date[0] == emo_date:
                    emotion = -1;

                    if fe[1] > 58:
                        emotion = 2
                    elif fe[1] > 46:
                        emotion = 1
                    else :
                        emotion = 0

                    if fc[6] >= 0:
                        df.loc[count] = (t,emotion, 1)
                    else:
                        df.loc[count] = (t, emotion, 0)
                    count += 1
df.to_csv("for_logistic.csv", encoding="UTF-8")