import pandas as pd

thema = ["게임","겨울"]#,"항공여행","자율주행차","인공지능"]

total = pd.read_csv("./Total.csv", usecols=[0,1,2], encoding="CP949")




for t in thema:
    df = pd.DataFrame(
        columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Change', '5Days', '10Days', '20Days', '60Days', '120Days', '종목코드',
                 '테마명', 'emotion'])
    cnt = 0
    for tv in total.values:
        if t == tv[2]:
            if not str(tv[0]).__contains__("테마"):
                temp = pd.read_csv(f"./sList/{tv[0]}.csv", encoding ="UTF-8")

                # count = 0
                # for code in temp.values:

    print(df)
    # df['Open'] //= count
    # df['High'] //= count
    # df['Low'] //= count
    # df['Close'] //= count
    # df['Volume'] //= count
    # df['Change'] /= count
    # df['5Days'] //= count
    # df['10Days'] //= count
    # df['20Days'] //= count
    # df['60Days'] //= count
    # df['120Days'] //= count
    # if df['emotion'] > 0:
    #     df['emotion'] = 1
    # elif df['emotion'] < 0:
    #     df['emotion'] = -1
    # df.to_csv(f"./sList/{tv[2]}테마.csv", header=True, encoding="UTF-8-sig")
