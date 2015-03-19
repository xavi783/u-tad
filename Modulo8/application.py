#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 17:28:20 2014

@author: xavi783
"""

import sys
sys.path.append('./modules')

import os
from tornado.web import Application, StaticFileHandler, RequestHandler
from tornado.ioloop import IOLoop, PeriodicCallback
from modules.data import main as data
from functools import partial

from tornado.log import enable_pretty_logging
enable_pretty_logging()

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "assets_path": os.path.dirname(__file__),
    "debug": True
}

class MainHandler(RequestHandler):
    def get(self):
        self.render("index.html", title="My title")

if __name__ == "__main__":
    application = Application([
        (r"/", MainHandler),
        (r"/datum/data.csv", data.StockHandler),
        (r"/correlation_data/", data.CorrelationHandler),
        (r"/(.*)", StaticFileHandler)
    ], **settings)
    application.listen(8888)
    main_loop = IOLoop.instance()
    main_loop.start()
