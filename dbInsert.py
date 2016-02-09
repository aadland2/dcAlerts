# -*- coding: utf-8 -*-
"""
Created on Wed Dec 02 08:00:26 2015

@author: aadlanma
"""
import psycopg2
conn = psycopg2.connect(database="AlertsDC", user="postgres", password="posgres")
cur = conn.cursor()

# cur.execute('''CREATE TABLE alerts (tweet_id bigint,created_at timestamp,body text, type text,symbol text,lat float,lon float);''')

tweets = [{'id':123,'created_at':"2015-06-26 13:44:55",'body':'Hello,tweet1','type':'violence','symbol':'#ff0000','lat':52.520074,'lon':-0.165842},
 {'id':124,'created_at':"2015-06-26 13:44:55",'body':'Hello,tweet2','type':'theft','symbol':'#ff9933','lat':52.541074,'lon':-0.166842},
 {'id':123,'created_at':"2015-06-26 13:44:55",'body':'Hello,tweet3','type':'traffic','symbol':' #ffff00','lat':52.542074,'lon':-0.167842}]

for tweet in tweets:
    data = (tweet['id'],tweet['created_at'],tweet['body'],tweet['type'],tweet['symbol'],tweet['lat'],tweet['lon'],)
    cur.execute('''INSERT INTO alerts VALUES (%s,%s,%s,%s,%s,%s,%s)''',data)
 
cur.execute('''UPDATE alerts SET geom = ST_SetSRID(ST_MakePoint(lon,lat),4326)''')
conn.commit()


cur.execute('''select * from alerts;''')
rows = cur.fetchall()