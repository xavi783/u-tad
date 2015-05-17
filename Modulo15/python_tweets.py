# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:09:06 2015

@author: jserrano
"""
import json
import tweepy
from collections import namedtuple, Counter
import nltk
import string
import pandas as pd
import numpy as np
import re
from nltk.stem import SnowballStemmer
from nltk.tag.stanford import POSTagger

Config = namedtuple("Config",["ConsumerKey","ConsumerSecret","AccessToken","AccessTokenSecret"])
config = Config(**json.load(open("config.json","r")))

auth = tweepy.OAuthHandler(config.ConsumerKey, config.ConsumerSecret)
auth.set_access_token(config.AccessToken, config.AccessTokenSecret)
api = tweepy.API(auth)

terms = 'PSOE'

#public_tweets = api.home_timeline()
#api.search(q=terms,lang='en',count=100)
 
corpus = u'\n'.join(np.r_[[[tweet.text for tweet in api.search(q=terms,lang='es',count=100)] for i in xrange(10)]].flat)
tokenizer = nltk.tokenize.WordPunctTokenizer()
tokens = tokenizer.tokenize(corpus)
#stemmer = SnowballStemmer("spanish")
#tokens = map(stemmer.stem,tokens)

tokenizer = nltk.tokenize.WhitespaceTokenizer()
tokens = np.r_[tokenizer.tokenize(corpus)]
is_url = np.r_[map(lambda x: any(re.findall('http:.',x)), tokens)]
urls = tokens[is_url]
is_user = np.r_[map(lambda x: any(re.findall('@.',x)), tokens)]
users = tokens[is_user]
is_hashtag = np.r_[map(lambda x: any(re.findall('#.',x)), tokens)]
hashtags = tokens[is_hashtag]
aux= np.unique(np.concatenate(map(lambda x: np.argwhere(x),[is_url,is_user,is_hashtag])))
aux = np.delete(tokens, aux)
tokenizer = nltk.tokenize.WordPunctTokenizer()
tokens = np.concatenate(np.r_[map(tokenizer.tokenize, aux)])
tokens = np.delete(tokens,np.argwhere(tokens==u'RT'))

model_path = './stanford-postagger/models/spanish.tagger'
jar_path = './stanford-postagger/stanford-postagger.jar'
spanish_postagger = POSTagger(model_path, jar_path, encoding='utf8') #, encoding='utf8'
tags = spanish_postagger.tag(tokens)

categories = ['nombre','adjetivo','verbo','determinante','puntuacion','preposiciones','otros']
y = (lambda x: x+[len(tags[0])-np.sum(x)])([np.sum([1 for w,t in tags[0] if t[0]==tp]) for tp in ['n','a','v','d','f','s']])
pd.DataFrame(y,index=categories,columns=['cat']).plot(kind='pie',y=['cat'],figsize=(5,5),legend=False,cmap=mpl.cm.Accent)