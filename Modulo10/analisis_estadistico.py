# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 15:08:35 2015

@author: jserrano
"""
#import numpy as np
#from sklearn.cross_validation import KFold, StratifiedKFold

import pandas as pd
import pickle as pkl
from scipy import stats as st 
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

DATA = pkl.load(open('indicators.pk','r'))
cur, ind, irs = DATA['cur'], DATA['ind'], DATA['irs']

ind_norm = pd.DataFrame(ind.pct_change()[1:],index=ind.index[1:],columns=['c1','c2'])
irs_norm = pd.DataFrame(irs.pct_change()[1:],index=irs.index[1:],columns=['c1','c2'])
close = pd.DataFrame(cur.pct_change()[1:],index=cur.index[1:],columns=['c'])
data = close.join(ind_norm.join(irs_norm,lsuffix='.ind',rsuffix='.irs'))
data.columns = ['c','ind1','ind2','irs1','irs2']
data['ind'] = (1+ind_norm['c1']/1+ind_norm['c2'])
data['irs'] = (1+irs_norm['c1']/1+irs_norm['c2'])
data['indB'] = (ind_norm['c1']-ind_norm['c2'])
data['irsB'] = (irs_norm['c1']-irs_norm['c2'])


#st.normaltest
#st.shapiro()
#st.f_oneway
f,axs = plt.subplots(2,2,figsize=(10,8))
for col,ax in zip(['ind1','ind2','irs1','irs2'],axs.flat):
    st.probplot(data[col], plot=ax)
    F,p = st.shapiro(data[col])
    ax.set_title('Probability Plot '+col.capitalize(),fontsize=10)
    ax.text(0.3, 0.7,'Shapiro:\n  W-score: {:.2f}\n  p-value: {:.2f}'.format(F,p), transform=ax.transAxes)
f.subplots_adjust(.09,.06,.97,.94,.2,.24)

ax = scatter_matrix(data[['c','ind','irs']],diagonal='kde')

lm_model = ols('c ~ ind*irs',data).fit()
print lm_model.summary2()

lm_model2 = ols('c ~ indB + irsB',data).fit()
print lm_model2.summary2()

independency_contrast = {0: lm_model, 1: lm_model2}
anova_lm(lm_model,lm_model2)

list(itt.combinations(xrange(4),2))


#def momentum(df):
#    moments,moments.index = pd.concat([df.mean(),df.std(),df.skew(),df.kurt()],1).T,['mean','std','skew','kurt']
#    return moments
#
#def get_statistics(df,df_norm,frequency='Y'):
#    if frequency=='M':
#        fhash = lambda x: map(dt,x.year,x.month,np.ones_like(x.month))
#    if frequency=='Y':
#        fhash = lambda x: map(dt,x.year,np.ones_like(x.year),np.ones_like(x.year))
#    gg = {'ret':df.pct_change().groupby(fhash(df.index)),
#          'norm':df_norm.groupby(fhash(df_norm.index))}
#    return gg, {k:v.apply(momentum).unstack(-1) for k,v in gg.iteritems()}
					