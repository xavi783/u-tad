# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 17:28:20 2014

@author: xavi783
"""

import json
import numpy as np
import pandas as pd
import pandas.io.data as web
import datetime as dt
from tornado.web import RequestHandler

START_DATE=dt.datetime(2000,1,1)
NAMES = ['AAPL','XOM','MSFT','JNJ','BRK.B','WFC','GE','PG','JPM','PFE']
symbols = pd.concat([web.get_data_yahoo(i, START_DATE)['Adj Close'] for i in NAMES],1)
symbols.columns = NAMES
symbols.index = [i.date() for i in list(symbols.index)]
symbols.index.names = ["date"]
panel_corr = pd.rolling_corr(symbols.pct_change(),21)
dates = np.array(map(lambda d: d.toordinal(), symbols.index))  

class StockHandler(RequestHandler):

    def get(self):
        self.write(symbols.to_csv())
        self.finish()

class CorrelationHandler(RequestHandler):

    encoder = json.JSONEncoder()

    def get_correlation(self,*date):
        f = lambda x: x[x<0][-1];
        find_date = lambda d,dates: list(np.argwhere(f((dates-dt.datetime(*d).toordinal()))==(dates-dt.datetime(*d).toordinal())).flat)[0]
        get_date = lambda d,dates: symbols.ix[find_date(d,dates)+[1,2],:].index[0]  
        return json.dumps((panel_corr[get_date(date,dates)].values).tolist())

    def post(self):
        fecha = tuple([int(i) for i in self.request.body.split("-")])
        self.write(self.encoder.encode(self.get_correlation(*fecha)))