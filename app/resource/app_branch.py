#!/usr/bin/env python2.7
#coding=utf-8
# Name: app_branch
# Function: branch api
# Date: 2016-06-23
# Email: day9011@gmail.com
import sys

from lib.db import Mydb

from flask.ext import restful
from lib.logging import create_logger
reload(sys)
sys.setdefaultencoding("utf-8")

logger = create_logger(__name__)

__all__ = ["branch_list"]

__author__ = 'day9011'

class branch_list(restful.Resource):
    def __init__(self):
        self.ret = {
            "status" : 0,
            "message": ""
        }
        self.db = Mydb()

    def get(self, project, domain, role):
        try:
            sql_str = 'SELECT DISTINCT branch FROM tag ' \
                      'WHERE project="%s" AND domain="%s" AND role="%s"' % (
                          project, domain, role)
            s, f = self.db.get(sql_str)
            print s, f
            if s:
                logger.error(f)
                raise Exception(str(f))
            print f
            self.ret['message'] = f
        except Exception, e:
            self.ret["status"] = -400
            self.ret["message"] = str(e)
        finally:
            return self.ret