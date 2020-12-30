import pandas as pd
import csv

def themeAverage() :
    themelist = ['게임', '겨울', '인공지능', '자율주행차', '항공여행']
    for k in themelist:
        sample = pd.read_csv(f'./작업/{k}.csv', usecols=[0, 1], encoding='cp949')
        namelist = []
        for m in sample.values:
            name = m[0]
            namelist.append(pd.read_csv(f'./작업/{name}.csv'))
        df = pd.DataFrame(
            columns=['Date', 'Open', 'High', 'Low', 'Close', '5Days', '10Days', '20Days', '60Days', '120Days', '종목코드',
                     '테마명'])
        df = namelist[0]
        del df['회사명']
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
            if k == '게임':
                df['종목코드'] = '123456'
            elif k == '겨울':
                df['종목코드'] = '234567'
            elif k == '항공여행':
                df['종목코드'] = '345678'
            elif k == '자율주행차':
                df['종목코드'] = '456789'
            else :
                df['종목코드'] = '567890'
            df['테마명'] = k
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
        df = df.iloc[-1]
        df1 = [str(df[0])[:10]]
        for j in range(1, len(df)):
            df1.append(df[j])
        fs = open(f'./작업/{k}테마.csv', 'a', newline='', encoding='utf-8-sig')
        wr = csv.writer(fs)
        wr.writerow(df1)
        fs.close()