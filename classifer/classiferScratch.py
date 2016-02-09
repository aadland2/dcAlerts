# -*- coding: utf-8 -*-
"""
Created on Thu Dec 03 10:35:43 2015

@author: aadlanma
"""
import pandas as pd
import sys
sys.path.append('C:\\Users\\aadlanma\\Desktop\\geocodingApp\\classifer')
from  twitter_helper import Tweet
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn import preprocessing



# train, test = train_test_split(df, test_size = 0.2)

df = pd.read_csv('C:\\Users\\aadlanma\\Desktop\\geocodingApp\\classifer\\alert_tweets.csv')


df_labeled =  df[pd.notnull(df['class '])]
X = [Tweet(x).clean_string() for x in df_labeled['text'].tolist()]
# X = df_labeled['text'].tolist()
lb = preprocessing.LabelEncoder()
Y_train = lb.fit_transform(df_labeled['class '].tolist())

X_train = np.array(X)




lb = preprocessing.LabelEncoder()
Yu = lb.fit_transform(df_labeled['class '].tolist())

classifier = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', OneVsRestClassifier(LinearSVC()))])

classifier.fit(X_train, Y_train)



import cPickle
# save the classifier
with open('alert_classifer.pkl', 'wb') as fid:
    cPickle.dump(classifier, fid)    


