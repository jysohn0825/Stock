import FinanceDataReader as fdr
import pandas as pd


sample = pd.read_csv("KOSPI+KOSDAQ.csv", usecols=[0, 2], encoding="CP949")
for i in sample.values:
    name = i[1]
    code = str(i[0])
    code = "0" * (6-len(code)) + code
    df = fdr.DataReader(code,"2020")
    df["종목코드"] = code
    min = df["Low"].min()
    if min <= 1000 and min > 100 and name.find("스팩") < 0:
        df.to_csv("coin.csv", mode="a", header = False)

