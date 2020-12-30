import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

for_logistic = pd.read_csv("for_logistic.csv", encoding="UTF-8", usecols=[2,3])

# feature_columns = for_logistic.columns.difference(["change"])
X = for_logistic["score"]
y = for_logistic["change"]

train_x, test_x ,train_y, test_y = train_test_split(X, y, stratify=y,train_size=0.7,test_size=0.3,random_state=1)
print(train_x.shape, test_x.shape, train_y.shape, test_y.shape)

# 로지스틱 모형 적합
model = sm.Logit(train_y, train_x)
results = model.fit(method = "newton")    # 다변수함수에 뉴턴방법을 적용한 로지스틱 회귀모형

print(results.summary())
