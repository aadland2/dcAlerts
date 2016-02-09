# -*- coding: utf-8 -*-
"""
Created on Wed Dec 02 12:34:45 2015

@author: aadlanma
"""
import addressRegex
lines = open('C:\\Users\\aadlanma\\Desktop\\geocodingApp\\alerts.txt','r').readlines()
texts2 = [addressRegex.slice_hours(text) for text in lines]
addresses = [addressRegex.regexWrapper(text) + ' Washington DC' for text in texts2]