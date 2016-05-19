# -*- coding: utf-8 -*-
"""
    logging
    ~~~~~~~

    Implements the logging support for ServiceCtrl.

    :copyright: (C) 2015 by Yu Jianjian
    :license: iqiyi.com
"""

from __future__ import absolute_import

import logging
from logging import (Formatter, getLogger, DEBUG)
from logging.handlers import RotatingFileHandler
from app import cfg
import os

# class ColorHandler(logging.StreamHandler):
#     LEVEL_COLORS = {
#         logging.DEBUG: '\033[00;32m',  # GREEN
#         logging.INFO: '\033[00;36m',  # CYAN
#         # logging.AUDIT: '\033[01;36m',  # BOLD CYAN
#         logging.WARN: '\033[01;33m',  # BOLD YELLOW
#         logging.ERROR: '\033[00;31m',  # RED
#         logging.CRITICAL: '\033[01;31m',  # BOLD RED
#     }

#     def format(self, record):
#         record.color = self.LEVEL_COLORS[record.levelno]
#         record_str = logging.StreamHandler.format(self, record)
#         return record.color + record_str


def create_logger(name, default=DEBUG):
    """ Create a customized logger.
    """
    log_file = cfg['log_file']
    log_path = os.path.dirname(log_file)
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    logger = getLogger(name)

    level = getattr(logging, cfg['log_level'], default)

    handler = RotatingFileHandler(log_file,
                                  maxBytes=1024000,
                                  backupCount=3)
    handler.setFormatter(Formatter(cfg['log_format']))

    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = 0

    return logger
