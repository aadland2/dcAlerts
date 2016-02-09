# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 14:01:04 2015

@author: aadlanma
"""
import re

from os import path

file_path = path.relpath("/geocodingApp")
# import os 
import sys
sys.path.append(path.dirname(__file__) + "/geocodingApp")
import commonRegex
street_address = re.compile(u'\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)', re.IGNORECASE)
intersection_string = re.compile('(?:\S+\s)?\S*(street|st|avenue|ave|Avenue|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)(.*)(street|st|avenue|Avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)\S*(?:\s\S+)',re.IGNORECASE)

endstring = re.compile('NE|NW|SE|SW|NE.|SE.|NW.|SW.')
# start string - number then space  b 
# intersections 'ave|avenue|street|st | ' at |ave|avenue|


# lines = open('C:\\Users\\aadlanma\\Desktop\\geocodingApp\\alerts.txt','r').readlines()

def slice_hours(text):
    p = re.search('(hrs|hours)',text)
    if p:
        return text[p.end():]
    else:
        return text 

        
        
def numeric_extract(i):
    p = re.search(r'\d+ b|\d+ \d',i)
    c = re.search('NW|SE|SW|NE',i)
    if p and c:
        return i[p.start():c.end()]

def alpha_extract(i):
    p = re.search(r'\d+ b|\d+ \d',i)
    c = re.search('(street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)',i)
    if p and c:
        return i[p.start():c.end()]
        
def intersection_extract(intersection_string,i):
    m = re.search(intersection_string,i)
    if m:
        c = re.search('NW|SE|SW|NE',i)
        if c:
            return i[m.start():c.end()]
        else:
            return i[m.start():m.end()]
        
def block_extract(i):
    p = re.search('(b/o|block of)',i)
    c = re.search('NW|SE|SW|NE',i)
    if p and c:
        return i[p.end():c.end()]
        
        
def regexWrapper(i):
    if numeric_extract(i):
        return numeric_extract(i) + ' Washington, DC'
    elif intersection_extract(intersection_string,i):
        return  intersection_extract(intersection_string,i) + ' Washington, DC'
    elif alpha_extract(i):
        return alpha_extract(i) + ' Washington, DC'
    elif block_extract(i):
        return  block_extract(i).strip() + ' Washington, DC'
    else:
        commoni = commonRegex.CommonRegex(i)
        if len(commoni.street_addresses) > 0:
            return commoni.street_addresses[0] + ' Washington, DC'
        else:
           return 'Washington, DC' 
        




# texts2 = [slice_hours(text) for text in lines]

# addresses = [regexWrapper(i) for i in texts2]
    
