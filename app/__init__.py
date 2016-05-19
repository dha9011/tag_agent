#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 17/2/16 PM3:32
# Copyright: TradeShift.com
__author__ = 'liming'

from flask import Flask
from flask.ext.restful import Api

from lib.conf_parser import init_config

cfg = init_config()

app = Flask(__name__)
api = Api(app)

from . import urls
