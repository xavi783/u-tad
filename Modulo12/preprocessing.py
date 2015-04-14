# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 16:32:51 2015

@author: x
"""
import sys
sys.path.append('/home/x/Documentos/python-toolbox')

import os,re
import urllib2
import numpy as np
import pandas as pd
from bs4 import  BeautifulSoup as bs4
from variables.variables import VarRepl
import matplotlib.pyplot as plt

ROOT = '/home/x/Documentos/'
if 'OS' in list(os.environ) and any(re.findall('^[wW]in.+',os.environ['OS'])):
#    ROOT = 'C:/Users/Xavi/Documents/u-tad/Modulo12/'
    ROOT = 'D:/Users/jserrano/Documents/u-tad/Modulo12/'
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

 # Preprocesado de datos
import matplotlib.pyplot as plt
from charts.generic import ticks2perc
# Comprobamos el número de NaNs por feature
nnans = lambda x: np.isnan(x).sum()/x.shape[0]

# Apreciamos que se distribuyen de manera muy similar, así que en un primer
# momento no los tendremos encuenta para construir el modelo, eliminando los
# clientes que presenten un NaN aquí, pero en todo caso, de tenerlos en cuenta
# realizaremos un muestreo estratificado para imputar los NaNs en #Dependants 
todrop = [traininig[np.isnan(traininig['NumberOfDependents'])].index, \
          traininig[np.isnan(traininig['SeriousDlqin2yrs'])].index]
trainB = traininig.copy()
for d in todrop:
    if any(d):
        trainB = trainB.drop(d)

# Análisis de los outliers de Dues
outliers1 = lambda x: trainB[var_groups.out][((trainB[var_groups.dues] > x*trainB[var_groups.dues].std()).sum(axis=1)>0)]
outliers2 = {0: lambda x: trainB[var_groups.out][trainB[var_groups.dues[0]] > x*trainB[var_groups.dues[0]].std()],
             1: lambda x: trainB[var_groups.out][trainB[var_groups.dues[1]] > x*trainB[var_groups.dues[1]].std()],
             2: lambda x: trainB[var_groups.out][trainB[var_groups.dues[2]] > x*trainB[var_groups.dues[2]].std()]}
#pd.Series(map(lambda x: (x.sum()/x.shape[0]).SeriousDlqin2yrs,[outliers1(n) for n in xrange(1,10)])).plot()
#pd.DataFrame({k: map(lambda x: (1.*x.sum()/len(x)).SeriousDlqin2yrs, [outliers2[k](n) for n in xrange(1,10)]) for k in xrange(3)}).plot()

# Debido a lo equilibrado que están las variables de salida respecto a los outliers
# de la estructura de Dues, creemos que no es el mejor onjunto de variables para
# probar modelos simples
import pickle as pkl
from sklearn.cross_validation import StratifiedKFold, KFold
from sklearn import metrics
KF = StratifiedKFold(np.r_[trainB[var_groups.out].values.flat], n_folds=5) # cada fold tiene un 10% del total
#
## balanceamos los test:
Fs = [f for f,k in KF]
Ks = [k for f,k in KF]
folds = {}
for i,k in enumerate(Ks):
    folds[i] = {'k':[],'f':Fs[i]}
    x = trainB[var_groups.out].iloc[k,:]
    xl = np.r_[(x==1).values.flat]
    subfolding_ratio = np.floor(1.*(x==0).sum()/(x==1).sum())[0]
    KF2 = KFold((x==0).sum()[0], subfolding_ratio)
    Ks2, Fs2 = [k2 for f2,k2 in KF2], [f2 for f2,k2 in KF2]
    for k2 in Ks2:
        folds[i]['k'] += [np.r_[k[k2],k[xl]]]

# Usando Random Forests:    
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

Classifiers = [RandomForestClassifier, KNeighborsClassifier, SVC, GaussianNB]
params = [dict(n_estimators=100, n_jobs=3), {}, {}, {}]
names = ['randomforest','knn','svm','naivebayes']

INS = np.r_[var_groups.dues,var_groups.familiarB,var_groups.loans]

class MultiClassifier(object):
    def __init__(self,dictClassifiers):
        self.__dict__.update(dictClassifiers)
        self.classifiers = dictClassifiers
        self.weights = np.ones(len(self.classifiers))/len(self.classifiers)
        
    def predict_proba(self,test,weigths=None):
        if type(weigths)!=type(None):
            self.weights = weigths
        p = [self.weights[i]*clf.predict_proba(test)[:,1] for i,clf in self.classifiers.iteritems()]
        p = np.r_[p].sum(0)
        return np.c_[np.arange(len(p)),p]

def build_classififers(Classifier, params, name):
    if ~os.path.exists(ROOT+name+'.pk'):   
        clf,P,mP,tP = {},{},{},{}
        INS = np.r_[var_groups.dues,var_groups.familiarB,var_groups.loans]
        OUT = var_groups.out
        for i,kf in folds.iteritems():        
            clf[i] = {x:Classifier(**params) for x in xrange(len(kf['k']))}
            for j,k in enumerate(kf['k']):
                clf[i][j].fit(trainB[INS].iloc[k].values, np.r_[trainB[OUT].iloc[k].values.flat])
            P[i] = np.c_[[forest.predict(trainB[INS].iloc[kf['f']]) for forest in clf[i].itervalues()]]   
            tP[i] = np.r_[trainB[OUT].iloc[kf['f']].values.flat]    
        roc = []
        # arboles equiponderados, cuando la imputación supera el treeshold, entonces se asigna clase =1, sino clase =0
        # máximo treeshold como óptimo    
        for treeshold in np.r_[0.:1.1:.1]:
            for i,kf in folds.iteritems():     
                mP[i] = P[i].sum(0)/(1.*P[i].shape[0])
                mP[i][mP[i]>treeshold],mP[i][mP[i]<=treeshold]=1,0
            roc += [np.mean([metrics.roc_auc_score(tp,p) for tp,p in zip(tP.itervalues(),mP.itervalues())])]    
        optimum = np.r_[roc].argmax()
        treeshold = np.r_[0.:1.1:.1][optimum]
        # Seleccionamos el conjunto de modelos óptimo entre todos los folds (con mejor roc) dado un treeshold óptimo
        for i,kf in folds.iteritems():     
            mP[i] = P[i].sum(0)/(1.*P[i].shape[0])
            mP[i][mP[i]>treeshold],mP[i][mP[i]<=treeshold]=1,0
        roc = np.r_[[metrics.roc_auc_score(tp,p) for tp,p in zip(tP.itervalues(),mP.itervalues())]]
        optimum = roc.argmax()
        pkl.dump(dict(clf=clf,P=P,tP=tP,mP=mP,treeshold=treeshold,optimum=optimum),open(ROOT+name+'.pk','w+'))    
    else:
        print 'Ya existe el archivo: '+ROOT+name+'.pk'
        
# Los mejores son: Random Forest y SVM:
def predict_proba(classifier, test):
    probs = [[index + 1, x[1]] for index, x in enumerate(classifier.predict_proba(test[INS]))]
    np.savetxt(ROOT+'submission.csv', probs, delimiter=',', fmt='%d,%f', header='Id,Probability', comments = '')
    return probs        

def plot_NaNs_info(caso,ax=None):
    if caso==1:
        if type(ax)==type(None):
            ax = nnans(traininig).plot(kind='bar',figsize=(10,6))
        else:
            nnans(traininig).plot(kind='bar',ax=ax)
        ax.set_xticklabels([VarRepl._retext(x.get_text(),replDict) for x in ax.get_xticklabels()],fontsize=10)
        plt.setp(ax.get_xticklabels(),rotation=30)
        ax.set_title('% of NaNs in training set')
        ticks2perc(ax,1,100,0)
    if caso==2:
        if type(ax)==type(None):
            ax = nnans(test).plot(kind='bar',figsize=(10,6))
        else:
            nnans(test).plot(kind='bar',ax=ax)
        ax.set_xticklabels([VarRepl._retext(x.get_text(),replDict) for x in ax.get_xticklabels()],fontsize=10)
        plt.setp(ax.get_xticklabels(),rotation=30)
        ax.set_title('% of NaNs in test set')
        ticks2perc(ax,1,100,0)
    if caso==3:
        # Dado que la salida es una variable booleana, comprobaremos como se distribuyen
        #  los NaN de #Dependants en cada clase
        gg = pd.DataFrame({k:nnans((traininig[(traininig[var_groups['out']]==k).values])) for k in [0,1]})
        if type(ax)==type(None):
            ax = gg.plot(kind='bar',figsize=(10,6))
        else:
            gg.plot(kind='bar',ax=ax)
        ax.set_xticklabels([VarRepl._retext(x.get_text(),replDict) for x in ax.get_xticklabels()],fontsize=10)
        plt.setp(ax.get_xticklabels(),rotation=30)
        ticks2perc(ax,1,100,0)
        ax.set_title('% of NaNs in Each Output Category, training set')
    if caso==4:
        # Dado que la salida es una variable booleana, comprobaremos como se distribuyen
        #  los NaN de #Dependants en cada clase
        gg = pd.DataFrame({k:nnans((test[(test[var_groups['out']]==k).values])) for k in [0,1]})
        if type(ax)==type(None):
            ax = gg.plot(kind='bar',figsize=(10,6))
        else:
            gg.plot(kind='bar',ax=ax)
        ax.set_xticklabels([VarRepl._retext(x.get_text(),replDict) for x in ax.get_xticklabels()],fontsize=10)
        plt.setp(ax.get_xticklabels(),rotation=30)
        ticks2perc(ax,1,100,0)
        ax.set_title('% of NaNs in Each Output Category, test set')
#         ax.get_figure().subplots_adjust(.055,.16,.97,.93)

#__main__
#__test__
if __name__=="__test__":

    map(build_classififers,Classifiers,params,names)
    auc = map(lambda name: (lambda d: metrics.roc_auc_score(d['tP'][d['optimum']],d['mP'][d['optimum']]))(pkl.load(open(ROOT+name+'.pk','r'))),names) 
    test.loc[np.isnan(test['NumberOfDependents']),'NumberOfDependents'] = np.mean(test.loc[~np.isnan(test['NumberOfDependents']),'NumberOfDependents'])
    
    d = pkl.load(open(ROOT+names[0]+'.pk','r'))
    d1 = pkl.load(open(ROOT+names[-1]+'.pk','r'))
    predict_proba(MultiClassifier(d['clf'][d['optimum']]),test)
    
    clasif2 = {k:v for k,v in enumerate(list(d['clf'][d['optimum']].itervalues())+list(d1['clf'][d1['optimum']].itervalues()))}
    predict_proba(MultiClassifier(clasif2),test)
    
    ## mxconfs = pd.concat([ pd.DataFrame(metrics.confusion_matrix(tp,p)) for tp,p in zip(tP.itervalues(),mP.itervalues())],0)
    ##http://www.bigdataexaminer.com/dealing-with-unbalanced-classes-svm-random-forests-and-decision-trees-in-python/