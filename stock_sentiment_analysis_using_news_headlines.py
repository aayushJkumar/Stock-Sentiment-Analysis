# -*- coding: utf-8 -*-
"""Stock Sentiment Analysis using News Headlines

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14L6zepEHvz2mO6naquo-aTzK8Nw4-t44
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np

data=pd.read_csv("/content/drive/MyDrive/Data.csv",encoding="ISO-8859-1")
data.head()

train = data[data['Date'] < '20150101']
test = data[data['Date'] > '20141231']

data=train.iloc[:,2:27]
data.replace("[^a-zA-Z]"," ",regex=True,inplace=True)
list1=[i for i in range(25)]
new_Index=[str(i) for i in list1]
data.columns= new_Index
data.head()

for index in new_Index:
  data[index]=data[index].str.lower()

data.head(5)

headlines=[]
for row in range(0,len(data.index)):
  headlines.append(' '.join(str(x) for x in data.iloc[row,0:25]))

headlines[0]

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

countvector=CountVectorizer(ngram_range=(2,2))
traindata=countvector.fit_transform(headlines)

from sklearn.feature_extraction.text import TfidfVectorizer
tv=TfidfVectorizer()
x=tv.fit_transform(headlines).toarray()
y=tv.fit_transform(headlines)

randomclassifier=RandomForestClassifier(n_estimators=200,criterion='entropy')
randomclassifier.fit(traindata,train['Label'])

test_transform= []
for row in range(0,len(test.index)):
    test_transform.append(' '.join(str(x) for x in test.iloc[row,2:27]))
test_dataset = countvector.transform(test_transform)
predictions = randomclassifier.predict(test_dataset)

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score

randomclassifier=RandomForestClassifier(n_estimators=500,criterion='entropy')
randomclassifier.fit(y,train['Label'])

test_transform_tv= []
for row in range(0,len(test.index)):
    test_transform_tv.append(' '.join(str(x) for x in test.iloc[row,2:27]))
test_dataset = tv.transform(test_transform_tv)
predictions_tv = randomclassifier.predict(test_dataset)

matrix=confusion_matrix(test['Label'],predictions)
print(matrix)
score=accuracy_score(test['Label'],predictions)
print(score)
report=classification_report(test['Label'],predictions)
print(report)

matrix=confusion_matrix(test['Label'],predictions_tv)
print(matrix)
score=accuracy_score(test['Label'],predictions_tv)
print(score)
report=classification_report(test['Label'],predictions_tv)
print(report)

