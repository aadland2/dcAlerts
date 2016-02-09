# -*- coding: utf-8 -*-
"""
Created on Fri Dec 04 12:30:02 2015

@author: aadlandma
"""
import psycopg2
conn = psycopg2.connect(database="SocialMedia", user="postgres", password="postgres")
cur = conn.cursor()
import sys
import numpy as np
import cPickle
import os 
import pandas as pd
sys.path.append(os.path.dirname(__file__) + "/classifer")
sys.path.append(os.path.dirname(__file__) + "/geocodingApp")
from twitter_helper import Tweet 
with open(os.path.dirname(__file__) + "/classifer" +'/alert_classifer.pkl', 'rb') as fid:
    classifier = cPickle.load(fid)
    
print 'packages loaded'
tweets = pd.read_csv('C:\\Users\\aadlandma\\Desktop\\geocodingApp\\classifer\\dcalerts_tweets2.csv')

# text = tweets['text'].tolist()
   
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

from addressRegex import regexWrapper 
import geocoder 


def geocode(text):
    try:
        latlng = geocoder.google(regexWrapper(text)).latlng
    except:
        latlng = []
    if not latlng:
        return [38.9071923, -77.0368707]
    else:
        return latlng
# cur.execute('''CREATE TABLE alerts (tweet_id bigint,created_at timestamp,body text, type text,symbol text,lat float,lon float);''')

#tweets = [{'id':123,'created_at':"2015-06-26 13:44:55",'body':'Hello,tweet1','type':'violence','symbol':'#ff0000','lat':52.520074,'lon':-0.165842},
# {'id':124,'created_at':"2015-06-26 13:44:55",'body':'Hello,tweet2','type':'theft','symbol':'#ff9933','lat':52.541074,'lon':-0.166842},
# {'id':123,'created_at':"2015-06-26 13:44:55",'body':'Hello,tweet3','type':'traffic','symbol':' #ffff00','lat':52.542074,'lon':-0.167842}]
#
#for tweet in tweets:
#    data = (tweet['id'],tweet['created_at'],tweet['body'],tweet['type'],tweet['symbol'],tweet['lat'],tweet['lon'],)
#    cur.execute('''INSERT INTO alerts VALUES (%s,%s,%s,%s,%s,%s,%s)''',data)

counter = 0
for index, row in tweets.iterrows():
    g = geocode(row['text'])
    c = label(classifier.predict(np.array([Tweet(row['text']).clean_string()])))
    data = (row['id'],row['created_at'],row['text'],c[0],c[1],g[0],g[1])
    cur.execute('''INSERT INTO alerts VALUES (%s,%s,%s,%s,%s,%s,%s)''',data)
    counter += 1
    conn.commit()
    print 'data inserted' + str(counter)


 
cur.execute('''UPDATE alerts SET geom = ST_SetSRID(ST_MakePoint(lon,lat),4326)''')
conn.commit()


cur.execute('''select * from alerts;''')
rows = cur.fetchall()
