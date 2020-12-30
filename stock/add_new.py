import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime, timedelta
TIME = datetime.today().strftime("%Y-%m-%d")
LAST_TIME = (datetime.today() - timedelta(180)).strftime("%Y-%m-%d")
import csv


def stockData():
    sample = pd.read_csv("./Total.csv", usecols=[0,1], encoding='cp949')
    for i in sample.values:
        name = i[0]
        code = str(i[1])
        code = "0" * (6 - len(code)) + code
        if name != '게임테마' and name != '겨울테마' and name != '자율주행차테마' and name != '항공여행테마' and name != '인공지능테마':
            df = fdr.DataReader(code, LAST_TIME, TIME)
            df['5Days'] = df['Close'].rolling(5).mean()
            df['10Days'] = df['Close'].rolling(10).mean()
            df['20Days'] = df['Close'].rolling(20).mean()
            df['60Days'] = df['Close'].rolling(60).mean()
            df['120Days'] = df['Close'].rolling(120).mean()
            df['종목코드'] = code
            df['회사명'] = name
            df = df.dropna()
            df.reset_index(drop=False, inplace=True)
            df = df.iloc[-1]
            df1 = [str(df[0])[:10]]
            for j in range(1,len(df)) :
                df1.append(df[j])
            fs = open(f'./작업/{name}.csv', 'a', newline='', encoding='utf-8-sig')
            wr = csv.writer(fs)
            wr.writerow(df1)
            fs.close()

stockData()