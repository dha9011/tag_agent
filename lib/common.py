#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 26/2/16 PM6:56
# Copyright: TradeShift.com
__author__ = 'liming'

import time
from logging import create_logger

logger = create_logger(__name__)

def cur_time(t_stamp=None):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t_stamp))

def retry(attempt):
    # decorator, need func return a status
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            result = (999, 'default')
            while att < attempt:
                try:
                    result = func(*args, **kw)
                    if isinstance(result, int):
                        status = result
                    elif isinstance(result, tuple):
                        status = result[0]
                    else:
                        raise Exception('Bad return format from func: %s, returns: %s' % (func, result))
                    if status:
                        raise Exception('Bad status return from func: %s, returns: %s' % (func, result))
                    else:
                        break
                except Exception as e:
                    logger.warning('Error in retry: %s' % str(e))
                    att += 1
                    time.sleep(1)
            return result
        return wrapper
    return decorator