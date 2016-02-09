# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 07:19:33 2015

@author: aadlandma
"""
from flask import Flask,render_template
app = Flask(__name__)
app.config['DEBUG'] = True
import psycopg2
import json 


try:
    conn = psycopg2.connect("dbname='SocialMedia' user='postgres' host='localhost' password='postgres'")
except:
    print "I am unable to connect to the database"


cur = conn.cursor()
#cur.execute('''select id, ST_AsGeoJSON(geom) from dc_tweets limit 10; ''')
#rows = cur.fetchall()

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
        


sql_string =''' SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features
        FROM (SELECT 'Feature' As type
        , ST_AsGeoJSON(lg.geom)::json As geometry
        , row_to_json((SELECT l FROM (SELECT body,symbol) As l
        )) As properties
        FROM alerts As lg  ) As f )  As fc; '''


def geojson_layer(sql_string):
    cur.execute(sql_string)
    rows = cur.fetchone()
    t = json.loads(json.dumps(rows[0]))
    tv = byteify(t)
    return tv
    

def event_dict(ids):
    layer_ids = []
    for e_id in ids:
        event_dict = {}
        cur.execute('''
        SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features
        FROM (SELECT 'Feature' As feat
        , ST_AsGeoJSON(lg.geom)::json As geometry
        , row_to_json((SELECT l FROM (SELECT type,body,symbol) As l
        )) As properties
        FROM alerts As lg  where type = %s) As f )  As fc;''', [e_id])
        rows = cur.fetchone()
        t = json.loads(json.dumps(rows[0]))
        tv = byteify(t)
        event_dict['id'] = 'ello' + str(e_id)
        event_dict['points'] = tv
        layer_ids.append(event_dict)
    return layer_ids



ids = ['theft','violence','closure']
layer_ids = event_dict(ids)
print layer_ids[1]

@app.route('/index')
def hello():
     ids = ['theft','violence','closure']
     layer_ids = event_dict(ids)
     print layer_ids[1]
   # remove type from sql string
   
     return render_template('EventToggle.html',layer_ids=layer_ids)
    

if __name__ == '__main__':
    app.run()



