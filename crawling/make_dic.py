import pandas as pd



df = pd.DataFrame(index=range(0,), columns=["word", "emoji"])
list = []
count = 0
sample = pd.read_csv("dic_emoji.csv", usecols=[0,1], encoding="UTF-8")
for i in sample.values:
    if i[0] not in list:
        df.loc[count] = (i[0],i[1])
        count+=1
        list.append(i[0])
df.to_csv("dictionary.csv")

