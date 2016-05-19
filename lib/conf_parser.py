#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 14/2/16 AM11:04
# Copyright: Tradeshift.com
__author__ = 'liming'

import yaml
import os
import sys

cfg = {}

def init_config():
    cur_dir = os.path.dirname(os.path.abspath(__file__))

    conf_file = cur_dir + '/../config.yml'

    if not os.path.isfile(conf_file):
        print 'Config file is not found: %s' % conf_file
        sys.exit(1)

    with open(conf_file, 'r') as f:
        global conf
        cfg = yaml.load(f.read())
    return cfg

# def get_config(key):
#     return cfg.get(key)

