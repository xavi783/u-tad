# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 16:32:51 2015

@author: x
"""
import os,re
import urllib2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import  BeautifulSoup as bs4
from charts.generic import ticks2perc
from variables.variables import VarRepl

ROOT = '/home/x/Documentos/'
if any(re.findall('^[wW]in.+',os.environ['OS'])):
    ROOT = 'C:/Users/Xavi/Documents/u-tad/Modulo12/'
path = 'https://xavi783.github.io/data/GiveMeSomeCredit/'

# Cargamos los datos y la agrupación de datos por categoría.

categories = ['dues','loans','familiar','out']
memory = bs4(urllib2.urlopen('https://github.com/xavi783/data/blob/master/GiveMeSomeCredit/memoria.md'))
#Creamos el diccionario de variables:
dv = {c:np.r_[map(lambda y: y.text.strip(),x.select('li'))] for c,x in zip(categories,memory.select("article[itemprop] .task-list")[2:])}
dv['familiarB'] = np.r_[list(set(dv['familiar']) - {u'MonthlyIncome'})]
replDict = [('NumberOf','#'),
            ('Number','#'),
            ('DaysPastDueNotWorse','DPastDue'),
            ('LinesAndLoans','Lines'),
            ('LoansOrLines','Loans'),
            ('RevolvingUtilizationOf','Util')]
var_groups = VarRepl(dv,replDict)
traininig = pd.read_csv(path+'cs-training.csv',index_col=0)
test = pd.read_csv(path+'cs-test.csv',index_col=0)

# # Preprocesado de datos

## Comprobamos el número de NaNs por feature
#nnans = lambda x: np.isnan(x).sum()/x.shape[0]
#ax = nnans(traininig).plot(kind='bar',figsize=(10,6))
#fig = ax.get_figure()
#ax.set_xticklabels([VarRepl._retext(x.get_text(),replDict) for x in ax.get_xticklabels()],fontsize=10)
#plt.setp(ax.get_xticklabels(),rotation=30)
#fig.suptitle('% of NaNs')
#fig.subplots_adjust(.055,.16,.97,.93)
#ticks2perc(ax,1,100,0)
#
## Dado que la salida es una variable booleana, comprobaremos como se distribuyen
##  los NaN de #Dependants en cada clase
#gg = pd.DataFrame({k:nnans((traininig[(traininig[var_groups['out']]==k).values])) for k in [0,1]})
#ax = gg.plot(kind='bar',figsize=(10,6))
#fig = ax.get_figure()
#ax.set_xticklabels([VarRepl._retext(x.get_text(),replDict) for x in ax.get_xticklabels()],fontsize=10)
#plt.setp(ax.get_xticklabels(),rotation=30)
#ticks2perc(ax,1,100,0)
#fig.suptitle('% of NaNs in Each Output Category')
#fig.subplots_adjust(.055,.16,.97,.93)

# Apreciamos que se distribuyen de manera muy similar, así que en un primer
# momento no los tendremos encuenta para construir el modelo, eliminando los
# clientes que presenten un NaN aquí, pero en todo caso, de tenerlos en cuenta
# realizaremos un muestreo estratificado para imputar los NaNs en #Dependants 

trainB = traininig[~np.isnan(traininig['NumberOfDependents'])].copy()

# Análisis de los outliers de Dues
outliers1 = lambda x: trainB[var_groups.out][((trainB[var_groups.dues] > x*trainB[var_groups.dues].std()).sum(axis=1)>0)]
outliers2 = {0: lambda x: trainB[var_groups.out][trainB[var_groups.dues[0]] > x*trainB[var_groups.dues[0]].std()],
             1: lambda x: trainB[var_groups.out][trainB[var_groups.dues[1]] > x*trainB[var_groups.dues[1]].std()],
             2: lambda x: trainB[var_groups.out][trainB[var_groups.dues[2]] > x*trainB[var_groups.dues[2]].std()]}
pd.Series(map(lambda x: (x.sum()/x.shape[0]).SeriousDlqin2yrs,[outliers1(n) for n in xrange(1,10)])).plot()
pd.DataFrame({k: map(lambda x: (1.*x.sum()/len(x)).SeriousDlqin2yrs, [outliers2[k](n) for n in xrange(1,10)]) for k in xrange(3)}).plot()

# Debido a lo equilibrado que están las variables de salida respecto a los outliers
# de la estructura de Dues, creemos que no es el mejor onjunto de variables para
# probar modelos simples
import pickle as pkl
import itertools as itt
from sklearn.cross_validation import StratifiedKFold
from sklearn import metrics

KF = StratifiedKFold(np.r_[trainB[var_groups.out].values.flat], n_folds=10) # cada fold tiene un 10% del total

# balanceamos los test:


# Usando SVMs:
from sklearn.svm import SVC

if ~os.path.exists(ROOT+'svcs.pk'):
    svcs,P,tP = {},{},{}
    for i,f,k in itt.izip(xrange(len(KF)),*itt.izip(*KF)):
        svcs[i] = SVC()
        svcs[i].fit(trainB[var_groups.familiarB].iloc[k].values, np.r_[trainB[var_groups.out].iloc[k].values.flat])
        P[i] = svcs[i].predict(trainB[var_groups.familiarB].iloc[f])
        tP[i] = np.r_[trainB[var_groups.out].iloc[f].values.flat]        
    mxconfs = pd.concat([pd.DataFrame(metrics.confusion_matrix(tp,p)) for tp,p in zip(tP.itervalues(),P.itervalues())],0)    
    pkl.dump(dict(svcs=svcs,P=P,tP=tP,KF=KF,mxconfs=mxconfs),open(ROOT+'svcs.pk','w+'))
else:
    data = pkl.dump(open(ROOT+'svcs.pk','r'))
    globals().update(data)

# Usando KNN:
from sklearn.neighbors import KNeighborsClassifier

if ~os.path.exists(ROOT+'kncs.pk'):    
    kncs,P,tP = {},{},{}
    for i,f,k in itt.izip(xrange(len(KF)),*itt.izip(*KF)):
        kncs[i] = KNeighborsClassifier()
        kncs[i].fit(trainB[var_groups.familiarB].iloc[k].values, np.r_[trainB[var_groups.out].iloc[k].values.flat])
        P[i] = kncs[i].predict(trainB[var_groups.familiarB].iloc[f])
        tP[i] = np.r_[trainB[var_groups.out].iloc[f].values.flat]    
    mxconfs = pd.concat([pd.DataFrame(metrics.confusion_matrix(tp,p)) for tp,p in zip(tP.itervalues(),P.itervalues())],0)    
    mxconfs = pkl.dump(dict(kncs=kncs,P=P,tP=tP,KF=KF,mxconfs=mxconfs),open(ROOT+'kncs.pk','w+'))
else:
    data = pkl.dump(open(ROOT+'kncs.pk','r'))
    globals().update(data)

# Usando Random Forests:    
from sklearn.ensemble import RandomForestClassifier

if ~os.path.exists(ROOT+'rfcs.pk'):   
    rfcs,P,tP = {},{},{}
    for i,f,k in itt.izip(xrange(len(KF)),*itt.izip(*KF)):
        rfcs[i] = RandomForestClassifier(n_estimators=10)
        rfcs[i].fit(trainB[var_groups.familiarB].iloc[k].values, np.r_[trainB[var_groups.out].iloc[k].values.flat])
        P[i] = kncs[i].predict(trainB[var_groups.familiarB].iloc[f])
        tP[i] = np.r_[trainB[var_groups.out].iloc[f].values.flat]
    
    mxconfs = pd.concat([pd.DataFrame(metrics.confusion_matrix(tp,p)) for tp,p in zip(tP.itervalues(),P.itervalues())],0)
    pkl.dump(dict(rfcs=rfcs,P=P,tP=tP,KF=KF,mxconfs=mxconfs),open(ROOT+'rfcs.pk','w+'))
else:
    data = pkl.dump(open(ROOT+'rfcs.pk','r'))
    globals().update(data)    

#http://www.bigdataexaminer.com/dealing-with-unbalanced-classes-svm-random-forests-and-decision-trees-in-python/