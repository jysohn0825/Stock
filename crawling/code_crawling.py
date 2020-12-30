import FinanceDataReader as fdr
import pandas as pd

df = pd.DataFrame(index=range(0,), columns=["code"])
count = 0

sample = pd.read_csv("KOSPI+KOSDAQ.csv", usecols=[0, 2], encoding="CP949")
for i in sample.values:
    name = i[1]
    code = str(i[0])
    code = "0" * (6-len(code)) + code
    temp = fdr.DataReader(code,"2020")
    min = temp["Low"].min()
    if min <= 1000 and min > 100 and name.find("스팩") < 0:
        df.loc[count] = code
        count += 1
df.to_csv("code.csv")



