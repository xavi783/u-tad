# -*- coding: utf-8 -*-
"""
Created on Sun May 17 11:54:47 2015

@author: x
"""
from __future__ import division
import re
import json
import nltk
import numpy as np
import pandas as pd
import matplotlib as mpl
from datetime import datetime
from collections import Counter
from nltk.tag.stanford import POSTagger

path = "./tweetsearch.out"
lines = [line.decode('utf-8').strip() for line in open(path,"r").readlines()]

decoder = json.JSONDecoder()
tweets = np.r_[map(decoder.decode,lines)]
lang = np.r_[map(lambda x: x['lang'], tweets)]

# filtramos por idioma para aplicar español
tweets_es = tweets[lang==u'es']
print "Los idiomas de los tweets son: [{}]".format(', '.join(np.unique(lang)))
print u"el % de tweets en español es: {:.2f}%".format(100*(len(tweets_es)/len(tweets)))

dtime = np.r_[ map(lambda x: datetime.strptime(x['created_at'],"%a %b %d %X +0000 %Y"), tweets_es)]
ix = np.r_[map(lambda x: x['id'],tweets_es)]
txt = np.r_[map(lambda x: unicode(x['text']),tweets_es)]
#tweet_text = np.r_[dtime,ix,txt]

txt_ct = Counter(txt)
mult = pd.Series([m for t,m in txt_ct.most_common()])

corpus = u'\n'.join([t for t,m in txt_ct.most_common()[:100]])
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