
# 데이터 불러오기
def read_data(filename):
    with open(filename, 'r', encoding="UTF-8") as f:
        data = [line.split("\t") for line in f.read().splitlines()]
        data = data[1:]
    return data

train_data = read_data("ratings_train.txt")
test_data = read_data("ratings_test.txt")


# 데이터 전처리
from konlpy.tag import Okt
import json
import os
from pprint import pprint

okt = Okt()

def tokenize(doc):
    #norm은 정규화 stem은 근어로 표시하기를 나타냄
    return ["/".join(t) for t in okt.pos(doc, norm=True, stem = True)]

if os.path.isfile("train_docs.json"):
    with open("train_docs.json", encoding="UTF-8") as f:
        train_docs = json.load(f)
    with open("test_docs.json", encoding="UTF-8") as f:
        test_docs = json.load(f)
else:
    train_docs = [(tokenize(row[1]),row[2]) for row in train_data]
    test_docs = [(tokenize(row[1]),row[2]) for row in test_data]
    with open("train_docs.json", 'w', encoding="UTF-8") as make_file:
        json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")
    with open("test_docs.json", 'w', encoding="UTF-8") as make_file:
        json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")
## 전처리
tokens = [t for d in train_docs for t in d[0]]
import nltk
text = nltk.Text(tokens, name = "NMSC")


## 자주 사용되는 토큰 10000개를 백터화
selected_words = [f[0] for f in  text.vocab().most_common(1000)]

def term_frequency(doc):
    return [doc.count(word) for word in selected_words]

train_x = [term_frequency(d) for d, _ in train_docs]
test_x = [term_frequency(d) for d, _ in test_docs]
train_y = [c for _, c in train_docs]
test_y = [c for _, c in test_docs]

import numpy as np

x_train = np.asarray(train_x).astype('float32')
x_test = np.asarray(test_x).astype('float32')

y_train = np.asarray(train_y).astype('float32')
y_test = np.asarray(test_y).astype('float32')


# 모델 정의 및 학슴
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras import metrics

model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(1000,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=optimizers.RMSprop(lr=0.001),
             loss=losses.binary_crossentropy,
             metrics=[metrics.binary_accuracy])

model.fit(x_train, y_train, epochs=10, batch_size=512)
results = model.evaluate(x_test, y_test)

def predict_pos_neg(review):
    token = tokenize(review)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(model.predict(data))
    if(score > 0.5):
        print("[{}]는 {:.2f}% 확률로 긍정 리뷰이지 않을까 추측해봅니다.^^\n".format(review, score * 100))
    else:
        print("[{}]는 {:.2f}% 확률로 부정 리뷰이지 않을까 추측해봅니다.^^;\n".format(review, (1 - score) * 100))

predict_pos_neg("올해 최고의 영화! 세 번 넘게 봐도 질리지가 않네요.")
predict_pos_neg("배경 음악이 영화의 분위기랑 너무 안 맞았습니다. 몰입에 방해가 됩니다.")
predict_pos_neg("주연 배우가 신인인데 연기를 진짜 잘 하네요. 몰입감 ㅎㄷㄷ")
predict_pos_neg("믿고 보는 감독이지만 이번에는 아니네요")
predict_pos_neg("주연배우 때문에 봤어요")