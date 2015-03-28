# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 16:32:51 2015

@author: x
"""
import string
import urllib2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import  BeautifulSoup as bs4
from charts.generic import ticks2perc

path = 'https://xavi783.github.io/data/GiveMeSomeCredit/'

# Cargamos los datos y la agrupación de datos por categoría.

categories = ['dues','loans','familiar','out']
memory = bs4(urllib2.urlopen('https://github.com/xavi783/data/blob/master/GiveMeSomeCredit/memoria.md'))
var_groups = {c:np.r_[map(lambda y: y.text.strip(),x.select('li'))] for c,x in zip(categories,memory.select("article[itemprop] .task-list")[2:])}

traininig = pd.read_csv(path+'cs-training.csv',index_col=0)
test = pd.read_csv(path+'cs-test.csv',index_col=0)

# # Preprocesado de datos

# Comprobamos el número de NaNs por feature
nnans = lambda x: np.isnan(x).sum()/x.shape[0]
def retext(s,X):
    for x in X: s = string.replace(s,*x)
    return s.strip()
replDict = [('NumberOf','#'),
            ('Number','#'),
            ('DaysPastDueNotWorse','DPastDue'),
            ('LinesAndLoans','Lines'),
            ('LoansOrLines','Loans'),
            ('RevolvingUtilizationOf','Util')]
ax = nnans(traininig).plot(kind='bar',figsize=(10,6))
fig = ax.get_figure()
ax.set_xticklabels([retext(x.get_text(),replDict) for x in ax.get_xticklabels()],fontsize=10)
plt.setp(ax.get_xticklabels(),rotation=30)
fig.suptitle('% of NaNs')
fig.subplots_adjust(.055,.16,.97,.93)
ticks2perc(ax,0,100,0)

# A continuación vamos a probar la imputación de NumberOfDependents, para eso
# vamos a muestrear el dataframe en función de forma estratificada en función del
# NumberOfDependents conocidos.



