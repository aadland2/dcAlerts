# -*- coding: utf-8 -*-
"""
Created on Wed Nov 04 06:50:37 2015

@author: aadlanma
"""
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
    
