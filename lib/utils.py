#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 17/2/16 PM3:58
# Copyright: TradeShift.com
__author__ = 'liming'

from flask.ext.restful import reqparse

def get_parser(arguments):
    parser = reqparse.RequestParser()
    for arg in arguments:
        parser.add_argument(arg)
    return parser