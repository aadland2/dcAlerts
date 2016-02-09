# -*- coding: utf-8 -*-
"""
Created on Thu Dec 03 14:50:49 2015

@author: aadlanma
"""

import sys
import numpy as np
import cPickle
import os 
import pandas as pd
from os import path

file_path = path.relpath("/geocodingApp")
sys.path.append(os.path.dirname(__file__) + "/classifer")
from os.path import dirname, realpath, sep, pardir
import sys
sys.path.append(dirname(realpath('/geocodingApp')) + sep + pardir + sep + "lib")

from twitter_helper import Tweet 

from geocodeAddress import geocode
with open(os.path.dirname(__file__) + "/classifer" +'/alert_classifer.pkl', 'rb') as fid:
    classifier = cPickle.load(fid)
    

tweets = pd.read_csv('C:\\Users\\aadlandma\\Desktop\\geocodingApp\\classifer\\alert_tweets.csv')

text = tweets['text'].tolist()
   
# g = classifier.predict(np.array([Tweet('oepn flesh wound resulting from a stabbing  stabbing in a robbery gone bad').clean_string()]))


def label(g):
    if 0 in g:
        return['advisory','#ffff00']
    elif 1 in g:
       return['closure','#ff0000']
    elif 2 in g:
        return['reopend','#33cc33']
    elif 3 in g:
        return['theft','#ff00ff']
    elif 4 in g:
        return['violence','#000000']

# v = labels(g)
classified = [classifier.predict(np.array([Tweet(x).clean_string()])) for x in text[0:10]]
pickup = [label(g) for g in classified]
truck = [geocode(t) for t in text[0:10]]


for index, row in tweets.iterrows():
    g = geocode(row['text'])
    c = label(classifier.predict(np.array([Tweet(row['text']).clean_string()])))