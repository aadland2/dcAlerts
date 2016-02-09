# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 07:19:33 2015

@author: aadlandma
"""
from flask import Flask,render_template
app = Flask(__name__)
# app.config['DEBUG'] = True
import json 
import os 

#try:
#    conn = psycopg2.connect("dbname='SocialMedia' user='postgres' host='localhost' password='postgres'")
#except:
#    print "I am unable to connect to the database"
#
#
#cur = conn.cursor()
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





@app.route('/')
def hello():
    sql_string =''' SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features
        FROM (SELECT 'Feature' As type
        , ST_AsGeoJSON(lg.geom)::json As geometry
        , row_to_json((SELECT l FROM (SELECT body,symbol) As l
        )) As properties
        FROM alerts As lg  ) As f )  As fc; '''
    # layer_ids = geojson_layer(sql_string)
    
    with open('result.json', 'r') as fp:
        layer_ids = json.load(fp)
   
    layer_ids = byteify(layer_ids)    
    # layer_ids = [
    # {'id':'fish','points':{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[-77.004139,38.947056]},"properties":{"id":"4444444444"}},{"type":"Feature","geometry":{"type":"Point","coordinates":[-79.1259979,37.32396829]},"properties":{"id":"665681331066642432"}}]}},
    # {'id':'pony','points':{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[-77.004139,38.947056]},"properties":{"id":"4444444444"}},{"type":"Feature","geometry":{"type":"Point","coordinates":[-79.1259979,37.32396829]},"properties":{"id":"665681331066642432"}}]}}]
    return render_template('geocodingIndex.html',layer_ids=layer_ids)
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run() 


