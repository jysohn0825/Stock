import pandas as pd
import csv
import math
import numpy as np

def themeAverage() :
    themelist = ['게임']#, '겨울', '인공지능', '자율주행차', '항공여행']
    for k in themelist:
        sample = pd.read_csv(f'./temp/{k}.csv', usecols=[0, 1], encoding='UTF-8')
        namelist = []
        for m in sample.values[:-1]:
            name = m[0]
            temp = pd.read_csv(f'./temp/{name}.csv', encoding="CP949")
            namelist.append(temp)
        df_columns = ['Date', 'Open', 'High', 'Low', 'Close', '5Days', '10Days', '20Days', '60Days', '120Days', 'emotion', 'count']
        df = pd.DataFrame(columns=df_columns)
        df = namelist[0]
        for i in range(0, len(namelist)):
            df['Date'] = namelist[i]['Date']
            df['Open'] += namelist[i]['Open']
            df['High'] += namelist[i]['High']
            df['Low'] += namelist[i]['Low']
            df['Close'] += namelist[i]['Close']
            df['Volume'] += namelist[i]['Volume']
            df['Change'] += namelist[i]['Change']
            df['5Days'] += namelist[i]['5Days']
            df['10Days'] += namelist[i]['10Days']
            df['20Days'] += namelist[i]['20Days']
            df['60Days'] += namelist[i]['60Days']
            df['120Days'] += namelist[i]['120Days']
            df['emotion'] += namelist[i]['emotion']
            df['count'] += namelist[i]['count']
        df['Open'] //= len(namelist)
        df['High'] //= len(namelist)
        df['Low'] //= len(namelist)
        df['Close'] //= len(namelist)
        df['Volume'] //= len(namelist)
        df['Change'] /= len(namelist)
        df['5Days'] /= len(namelist)
        df['10Days'] /= len(namelist)
        df['20Days'] /= len(namelist)
        df['60Days'] /= len(namelist)
        df['120Days'] /= len(namelist)
        df['emotion'] /= len(namelist)
        df['count'] //= len(namelist)
        count = 0
        for i in df['emotion'].values:
            if i > 0:
                df.loc[count, 'emotion'] = 1
            elif i < 0:
                df.loc[count, 'emotion'] = -1
            else:
                df.loc[count, 'emotion'] = 0
            count += 1
        df = df.iloc[-1]
        df1 = []
        for j in df_columns:
            df1.append(df[j])
        fs = open(f'./{k}테마.csv', 'a', newline='', encoding='utf-8-sig')
        wr = csv.writer(fs)
        wr.writerow(df1)
        fs.close()

themeAverage()