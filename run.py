#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 11/2/16 PM12:19
# Copyright: Tradeshift.com
__author__ = 'liming'

# from runner import run
#
# if __name__ == '__main__':
#     run()
#

from app import app, cfg

if __name__ == '__main__':
    app.run(host=cfg['listen_addr'], port=cfg['listen_port'], debug=cfg['debug'])


