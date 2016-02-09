# -*- coding: utf-8 -*-
"""
Created on Fri Dec 04 07:55:20 2015

@author: aadlandma
"""
from addressRegex import regexWrapper 
import geocoder 


def geocode(text):
    try:
        latlng = geocoder.bing(regexWrapper(text)).latlng
    except:
        latlng = []
    if not latlng:
        return [38.9071923, -77.0368707]
    else:
        return latlng
 
geocode('Stabbing in the 600 b/o Edgewood St NE. No lookout. CALL 911 W/ EVENT #I20150697501')