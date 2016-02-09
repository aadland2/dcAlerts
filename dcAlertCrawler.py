# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 12:17:56 2015

@author: aadlandma
"""

#### import boilerplate ####
import sys
import numpy as np
import cPickle
import os 
from os import path
file_path = path.relpath("/geocodingApp")
sys.path.append(os.path.dirname("/geocodingApp") + "/classifer")
from os.path import dirname, realpath, sep, pardir
import sys
sys.path.append(dirname(realpath('/geocodingApp')) + sep + pardir + sep + "lib")

#### import tweepy and open up database  #### 

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sys
import json
import psycopg2

connection = psycopg2.connect("dbname=SocialMedia user=postgres password=postgres host=localhost")
cursor = connection.cursor()
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

def reset_cursor():
    cursor = connection.cursor()






    


# Tokens 
access_token = "2600054148-vbUOJ0Oe23IUvaMjSgZWtTJHDjQWqR2ZDJn8i8f"
access_token_secret = "EKk6B69zlehQIQmndEJPorhR3b2SLk3tUFP9oeJH9o23f"
consumer_key = "97h2n7avgkJp4snsNXm0RMaTB"
consumer_secret = "fjT8sdgLTMkYOg9N8GrXU0cGwGUSyH3CbwD33V8jswTJJdcQr3"

#consumer key, consumer secret, access token, access secret.
ckey= consumer_key
csecret= consumer_secret
atoken= access_token
asecret= access_token_secret



#### Tweet Class ####
import nltk
from nltk.corpus import stopwords 
custom = ['wind','wpm','temp','amp','tmp','trends','weather','mph','today','wsw','solar','gust','rain',
          'download','hrs','humidity','london','pressure','forecast','precipitation','hum','.mph',
           'barometer','temperature','hpa','cloud','day','happy','rising','.hpa','.mm\'','am',"'m",'at',
           'ave','bad','beautiful','best','better','big','bit','boy','come','coming','days','fee','feels','fine','home','hot','left','let','light','like','little','live',"'ll",'lol','look','looking','lot',
           'nice','new','news','nnw','pre','read','seeing','seen','sure','trending',"'ve",'yes','went','win','want','way','wow',
           "n't",'great','amazing','awesome','bad','big','day','days','feel','got','happy','set','slow','thanks','tonight',
           'great','day','good','photo','look','like',"'m","m", ' at','london','new']
          
          
utf = map(unicode,custom)
stops = list(stopwords.words("english"))
v = list(stops)
v.extend(utf)

stops = set(v)
class Tweet(str):
    ''' Class object to handle Tweets 
    Methods defined are:
    
        checkin(...) --> bool
        returns true if the tweet is a checkin 
        
        clean_string(...) --> string
        returns a tweet with the hastags, mentions,stopwords, 
            and non-string characters removed  
        
        hashtags(...) --> string 
        returns a string of hashtags in the tweet
        
        count_tags(...) --> int
        returns the count of hashtags in the string 
        
        mentions(...) --> string
        returns a string of mentions in the tweet
        
        count_mentions(...) --> int 
        returns a count of mentions in the sting 
        
        links(...) --> list
        returns a list links in the string 
        
        count_links(...) --> int
        returns a count of the links  '''
    
    
    def __init__(self,text):
        self.text = text
    
    def checkin(self):
        text = self
        return text.startswith("I'm at")
        
    def clean_string(self):
        text = self.lower()
        text = ''.join(i for i in text if not i.isdigit())
        text = ' '.join([i for i in text.split() if i.isalpha()])
        tokens = [word for word in nltk.word_tokenize(text)]
        tokens = [token for token in tokens if token not in stops and len(token) > 2]
        return ' '.join(tokens)
        
    def hashtags(self):
        text = self.lower()
        return  [i  for i in text.split() if i.startswith("#")]
        
    def count_tags(self):
        text = self 
        return  len([i  for i in text.split() if i.startswith("#")])
    
    def mentions(self):
        text = self 
        return  ' '.join([i  for i in text.split() if i.startswith("@")]) 
        
    def count_mentions(self):
        text = self 
        return len([i  for i in text.split() if i.startswith("@")])
    
    def links(self):
        text = self
        return  [i  for i in text.split() if i.startswith("http")] 
    
    def count_links(self):
        text = self 
        return  len([i  for i in text.split() if i.startswith("http")])
        
    def tokens(self):
        v = []
        text = self.lower()
        hashtags = [i  for i in text.split() if i.startswith("#") ]
        text = ' '.join([i for i in text.split() if i.isalpha()])
        tokens = list(set([word for word in nltk.word_tokenize(text)]))
        tokens = [token for token in tokens if token not in stops and len(token) > 2]
        v.extend(tokens)
        v.extend(hashtags)
        return v



def join_elements(tokens,hashtags):
    '''a function to join the elements of a tweet '''
    v = []
    v.extend(tokens)
    v.extend(hashtags)
    return ' '.join(v)
    
#### End Tweet #### 

#### Geocoder #### 
from types import MethodType
import re
import geocoder 


#### Portion borrowed from common regex project on github https://github.com/madisonmay/CommonRegex
date           = re.compile(u'(?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4}', re.IGNORECASE)
time           = re.compile(u'\d{1,2}:\d{2} ?(?:[ap]\.?m\.?)?|\d[ap]\.?m\.?', re.IGNORECASE)
phone          = re.compile(u'((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))')
link           = re.compile(u'(?i)((?:https?://|www\d{0,3}[.])?[a-z0-9.\-]+[.](?:(?:international)|(?:construction)|(?:contractors)|(?:enterprises)|(?:photography)|(?:immobilien)|(?:management)|(?:technology)|(?:directory)|(?:education)|(?:equipment)|(?:institute)|(?:marketing)|(?:solutions)|(?:builders)|(?:clothing)|(?:computer)|(?:democrat)|(?:diamonds)|(?:graphics)|(?:holdings)|(?:lighting)|(?:plumbing)|(?:training)|(?:ventures)|(?:academy)|(?:careers)|(?:company)|(?:domains)|(?:florist)|(?:gallery)|(?:guitars)|(?:holiday)|(?:kitchen)|(?:recipes)|(?:shiksha)|(?:singles)|(?:support)|(?:systems)|(?:agency)|(?:berlin)|(?:camera)|(?:center)|(?:coffee)|(?:estate)|(?:kaufen)|(?:luxury)|(?:monash)|(?:museum)|(?:photos)|(?:repair)|(?:social)|(?:tattoo)|(?:travel)|(?:viajes)|(?:voyage)|(?:build)|(?:cheap)|(?:codes)|(?:dance)|(?:email)|(?:glass)|(?:house)|(?:ninja)|(?:photo)|(?:shoes)|(?:solar)|(?:today)|(?:aero)|(?:arpa)|(?:asia)|(?:bike)|(?:buzz)|(?:camp)|(?:club)|(?:coop)|(?:farm)|(?:gift)|(?:guru)|(?:info)|(?:jobs)|(?:kiwi)|(?:land)|(?:limo)|(?:link)|(?:menu)|(?:mobi)|(?:moda)|(?:name)|(?:pics)|(?:pink)|(?:post)|(?:rich)|(?:ruhr)|(?:sexy)|(?:tips)|(?:wang)|(?:wien)|(?:zone)|(?:biz)|(?:cab)|(?:cat)|(?:ceo)|(?:com)|(?:edu)|(?:gov)|(?:int)|(?:mil)|(?:net)|(?:onl)|(?:org)|(?:pro)|(?:red)|(?:tel)|(?:uno)|(?:xxx)|(?:ac)|(?:ad)|(?:ae)|(?:af)|(?:ag)|(?:ai)|(?:al)|(?:am)|(?:an)|(?:ao)|(?:aq)|(?:ar)|(?:as)|(?:at)|(?:au)|(?:aw)|(?:ax)|(?:az)|(?:ba)|(?:bb)|(?:bd)|(?:be)|(?:bf)|(?:bg)|(?:bh)|(?:bi)|(?:bj)|(?:bm)|(?:bn)|(?:bo)|(?:br)|(?:bs)|(?:bt)|(?:bv)|(?:bw)|(?:by)|(?:bz)|(?:ca)|(?:cc)|(?:cd)|(?:cf)|(?:cg)|(?:ch)|(?:ci)|(?:ck)|(?:cl)|(?:cm)|(?:cn)|(?:co)|(?:cr)|(?:cu)|(?:cv)|(?:cw)|(?:cx)|(?:cy)|(?:cz)|(?:de)|(?:dj)|(?:dk)|(?:dm)|(?:do)|(?:dz)|(?:ec)|(?:ee)|(?:eg)|(?:er)|(?:es)|(?:et)|(?:eu)|(?:fi)|(?:fj)|(?:fk)|(?:fm)|(?:fo)|(?:fr)|(?:ga)|(?:gb)|(?:gd)|(?:ge)|(?:gf)|(?:gg)|(?:gh)|(?:gi)|(?:gl)|(?:gm)|(?:gn)|(?:gp)|(?:gq)|(?:gr)|(?:gs)|(?:gt)|(?:gu)|(?:gw)|(?:gy)|(?:hk)|(?:hm)|(?:hn)|(?:hr)|(?:ht)|(?:hu)|(?:id)|(?:ie)|(?:il)|(?:im)|(?:in)|(?:io)|(?:iq)|(?:ir)|(?:is)|(?:it)|(?:je)|(?:jm)|(?:jo)|(?:jp)|(?:ke)|(?:kg)|(?:kh)|(?:ki)|(?:km)|(?:kn)|(?:kp)|(?:kr)|(?:kw)|(?:ky)|(?:kz)|(?:la)|(?:lb)|(?:lc)|(?:li)|(?:lk)|(?:lr)|(?:ls)|(?:lt)|(?:lu)|(?:lv)|(?:ly)|(?:ma)|(?:mc)|(?:md)|(?:me)|(?:mg)|(?:mh)|(?:mk)|(?:ml)|(?:mm)|(?:mn)|(?:mo)|(?:mp)|(?:mq)|(?:mr)|(?:ms)|(?:mt)|(?:mu)|(?:mv)|(?:mw)|(?:mx)|(?:my)|(?:mz)|(?:na)|(?:nc)|(?:ne)|(?:nf)|(?:ng)|(?:ni)|(?:nl)|(?:no)|(?:np)|(?:nr)|(?:nu)|(?:nz)|(?:om)|(?:pa)|(?:pe)|(?:pf)|(?:pg)|(?:ph)|(?:pk)|(?:pl)|(?:pm)|(?:pn)|(?:pr)|(?:ps)|(?:pt)|(?:pw)|(?:py)|(?:qa)|(?:re)|(?:ro)|(?:rs)|(?:ru)|(?:rw)|(?:sa)|(?:sb)|(?:sc)|(?:sd)|(?:se)|(?:sg)|(?:sh)|(?:si)|(?:sj)|(?:sk)|(?:sl)|(?:sm)|(?:sn)|(?:so)|(?:sr)|(?:st)|(?:su)|(?:sv)|(?:sx)|(?:sy)|(?:sz)|(?:tc)|(?:td)|(?:tf)|(?:tg)|(?:th)|(?:tj)|(?:tk)|(?:tl)|(?:tm)|(?:tn)|(?:to)|(?:tp)|(?:tr)|(?:tt)|(?:tv)|(?:tw)|(?:tz)|(?:ua)|(?:ug)|(?:uk)|(?:us)|(?:uy)|(?:uz)|(?:va)|(?:vc)|(?:ve)|(?:vg)|(?:vi)|(?:vn)|(?:vu)|(?:wf)|(?:ws)|(?:ye)|(?:yt)|(?:za)|(?:zm)|(?:zw))(?:/[^\s()<>]+[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019])?)', re.IGNORECASE)
email          = re.compile(u"([a-z0-9!#$%&'*+\/=?^_`{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)", re.IGNORECASE)
ip             = re.compile(u'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', re.IGNORECASE)
ipv6           = re.compile(u'\s*(?!.*::.*::)(?:(?!:)|:(?=:))(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)){6}(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)[0-9a-f]{0,4}(?:(?<=::)|(?<!:)|(?<=:)(?<!::):)|(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)){3})\s*', re.VERBOSE|re.IGNORECASE|re.DOTALL)
price          = re.compile(u'[$]\s?[+-]?[0-9]{1,3}(?:(?:,?[0-9]{3}))*(?:\.[0-9]{1,2})?')
hex_color      = re.compile(u'(#(?:[0-9a-fA-F]{8})|#(?:[0-9a-fA-F]{3}){1,2})\\b')
credit_card    = re.compile(u'((?:(?:\\d{4}[- ]?){3}\\d{4}|\\d{15,16}))(?![\\d])')
btc_address    = re.compile(u'(?<![a-km-zA-HJ-NP-Z0-9])[13][a-km-zA-HJ-NP-Z0-9]{26,33}(?![a-km-zA-HJ-NP-Z0-9])')
street_address = re.compile(u'\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)', re.IGNORECASE)

regexes = {"dates"            : date,
           "times"            : time,
           "phones"           : phone,
           "links"            : link,
           "emails"           : email,
           "ips"              : ip,
           "ipv6s"            : ipv6,
           "prices"           : price,
           "hex_colors"       : hex_color,
           "credit_cards"     : credit_card,
           "btc_addresses"    : btc_address,
           "street_addresses" : street_address }

class regex:

  def __init__(self, obj, regex):
    self.obj = obj
    self.regex = regex

  def __call__(self, *args):
    def regex_method(text=None):
      return [x.strip() for x in self.regex.findall(text or self.obj.text)]
    return regex_method

class CommonRegex(object):

    def __init__(self, text=""):
        self.text = text

        for k, v in regexes.items():
          setattr(self, k, regex(self, v)(self))

        if text:
            for key in regexes.keys():
                method = getattr(self, key)
                setattr(self, key, method())





intersection_string = re.compile('(?:\S+\s)?\S*(street|st|avenue|ave|Avenue|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)(.*)(street|st|avenue|Avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)\S*(?:\s\S+)',re.IGNORECASE)

endstring = re.compile('NE|NW|SE|SW|NE.|SE.|NW.|SW.')


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
        commoni = CommonRegex(i)
        if len(commoni.street_addresses) > 0:
            return commoni.street_addresses[0] + ' Washington, DC'
        else:
           return 'Washington, DC' 
        

def geocode(text):
    try:
        latlng = geocoder.google(regexWrapper(text)).latlng
    except:
        latlng = []
    if not latlng:
        return [38.9071923, -77.0368707]
    else:
        return latlng

#### End Geocoder #### 

#### Classifier #### 
with open(os.getcwd() + "/classifer" +'/alert_classifer.pkl', 'rb') as fid:
    classifier = cPickle.load(fid)


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

# c = 'Robbery Gun at 0510 hrs in the 2400 b/o Alabama Avenue SE. LOF a B/M, red tennis shoes and black jacket CALL 911 W/ EVENT # I20150690310' 
# gg = classifier.predict(np.array([Tweet(c).clean_string()]))

#### End Classifer 



class listener(StreamListener):

    def on_data(self, data):
        d = json.loads(data)
        try:
            c = ''.join(d["text"].splitlines())
            classified = classifier.predict(np.array([Tweet(c).clean_string()]))
            event_label = label(classified)
            g = geocode(c)
            data = (d['id'],d['created_at'],c,event_label[0],event_label[1],g[0],g[1])
            cursor.execute('''INSERT INTO alerts VALUES (%s,%s,%s,%s,%s,%s,%s)''',data)
            cursor.execute('''UPDATE alerts SET geom = ST_SetSRID(ST_MakePoint(lon,lat),4326)''')
            connection.commit()
            print 'insert success'
        except UnicodeEncodeError:
            'out of range unicode character' 
 

    def on_error(self, status):
        print status
        return True 
        
    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True 

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(follow=['15273747']) 

