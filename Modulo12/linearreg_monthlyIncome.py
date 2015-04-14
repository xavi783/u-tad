# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 15:28:37 2015

@author: jserrano
"""
import numpy as np
import pandas as pd
import seaborn as sns
from pandas import DataFrame as df_
from pandas.tools.plotting import scatter_matrix

corrmat = trainB[np.r_[INS,'MonthlyIncome']].corr()

axs = scatter_matrix(trainB[np.r_[INS,['MonthlyIncome']]])
for ax in axs[:,0]: ax.set_ylabel(ax.get_ylabel(),rotation=0)
for ax in axs[-1,:]: ax.set_xlabel(ax.get_xlabel(),rotation=10)
    
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler as ZScore
zscore = ZScore()
pca = PCA(n_components=2)
#INS2 = np.r_[INS,['MonthlyIncome']]
INS2 = np.r_[var_groups.familiarB,var_groups.loans]

x = trainB[INS2][~np.isnan(trainB.MonthlyIncome)]
pca.fit(zscore.fit_transform(x))

def plot_components():
    f, axs = plt.subplots(1,3,figsize=(16,3))
    ax = df_(pca.components_.T,index=INS2).plot(kind='scatter',x=0,y=1,ax=axs[0],title="compoonents without dues")
    txts = [ax.text(v[1][0],v[1][1],k) for k,v in zip(names_INS2,df_(pca.components_.T,index=INS2).iterrows())]
        
    x = trainB[INS2][~np.isnan(trainB.MonthlyIncome)]
    pca7 = PCA(n_components=len(INS2))
    pca7.fit(zscore.fit_transform(x))
    df_(pca7.explained_variance_).plot(ax=axs[1],title="without dues")
    
    x = trainB[np.r_[INS,['MonthlyIncome']]][~np.isnan(trainB.MonthlyIncome)]
    pca7b = PCA(n_components=len(INS2))
    pca7b.fit(zscore.fit_transform(x))
    df_(pca7b.explained_variance_).plot(ax=axs[2],title="with dues")
    
    return  ', '.join([x.get_text() for x in txts])

# Regresión lineal:
INS = np.r_[var_groups.familiarB,var_groups.loans]    
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lma = lm.fit(trainB[INS][~np.isnan(trainB.MonthlyIncome)],trainB['MonthlyIncome'][~np.isnan(trainB.MonthlyIncome)])
