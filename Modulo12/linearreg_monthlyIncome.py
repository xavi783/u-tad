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
INS2 = np.r_[var_groups.familiar,var_groups.loans]

x = trainB[INS2][~np.isnan(trainB.MonthlyIncome)]
pca.fit(zscore.fit_transform(x))

ax = df_(pca.components_.T,index=INS2).plot(kind='scatter',x=0,y=1)
[ax.text(v[0],v[1],k[-5:]) for k,v in df_(pca.components_.T,index=INS2).iterrows()]