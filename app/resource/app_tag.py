#!/usr/bin/env python2.7
#coding=utf-8
__author__ = 'day9011'

import sys

from lib.db import Mydb

from flask.ext import restful
from flask.ext.restful.reqparse import Argument as Arg

from lib.logging import create_logger
from flask import request
from lib.utils import get_parser
import re
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

logger = create_logger(__name__)

__all__ = ["tag_submit", "tag_url", "tag_list"]

def url_is_correct(url):
    if re.match(r'^https?:/{2}.*?$', url):
        return True
    else:
        return False

class tag_submit(restful.Resource):
    def __init__(self):
        self.ret = {
            "status": 0,
            "message": ""
        }
        self.db = Mydb()

    def post(self):
        #判断post的值是否正确
        try:
            arguments = [
                Arg('tag', type=str, required=True, help='Miss tag'),
                Arg('domain', type=str, required=False, help='Miss domain', default=""),
                Arg('project', type=str, required=True, help='Miss project'),
                Arg('role', type=str, required=True, help='Miss role'),
                Arg('comment', type=str, required=True, help='Miss comment'),
                Arg('commit_time', type=str, required=True, help='Miss commit_time'),
                Arg('commit_user', type=str, required=True, help='Miss commit_user'),
                Arg('download_url', type=str, required=True, help='Miss download_url'),
                Arg('config_url', type=str, required=True, help='Miss config_url'),
                Arg('is_ready', type=str, required=False, help='Miss is_ready', default=""),
                Arg('branch', type=str, required=True, help='Miss is_ready'),
            ]
            args = get_parser(arguments).parse_args()
            tag_tag = args['tag']
            tag_domain = args['domain']
            tag_project = args['project']
            tag_role = args['role']
            tag_comment = args['comment']
            tag_commit_time = args['commit_time']
            tag_commit_user = args['commit_user']
            tag_download_url = args['download_url']
            tag_config_url = args['config_url']
            tag_is_ready = args['is_ready']
            tag_branch = args['branch']
            #判断此tag值是否已经存在
            sql_str = 'SELECT tag FROM tag WHERE tag="%s" and project="%s" and role="%s" and branch="%s"' % (
                        tag_tag, tag_project, tag_role, tag_branch)
            exist_tag, f = self.db.get(sql_str)
            if exist_tag:
                raise Exception("this tag is exist")
            ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
            try:
                #将提交时间的字符转转化成datetime格式
                tag_commit_time = datetime.datetime.strptime(tag_commit_time, ISOTIMEFORMAT)
            except Exception, e:
                raise Exception(str(e))
            print tag_commit_time
            sql_str = 'INSERT INTO tag (tag, domain, project, role, comment, commit_time, commit_user, config_url, download_url, is_ready, branch) ' \
                      'VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' % (
                tag_tag, tag_domain, tag_project, tag_role, tag_comment, tag_commit_time, tag_commit_user, tag_config_url, tag_download_url, tag_is_ready, tag_branch)
            s, f = self.db.modify(sql_str)
            if s:
                logger.error(f)
                raise Exception(str(f))
            self.ret['message'] = "OK"
            logger.info('insert a tag info: %s', self.ret["message"])
        except Exception, e:
            logger.error(str(e))
            self.ret["status"] = -400
            self.ret["message"] = str(e)
        finally:
            return self.ret

class tag_list(restful.Resource):
    def __init__(self):
        self.ret = {
            "status" : 0,
            "message": ""
        }
        self.db = Mydb()

    def get(self, project, domain, branch, role):
        try:
            tag_limit = request.args.get('limit')
            if not tag_limit:
                raise Exception("Miss limit")
            if not tag_limit.isdigit():
                raise Exception("limit is not a digit")
            sql_str = 'SELECT tag,comment, commit_time,commit_user FROM tag ' \
                      'WHERE project="%s" AND domain="%s" AND branch="%s" AND role="%s" ORDER BY commit_time DESC LIMIT %d' % (
                       project, domain, branch, role, int(tag_limit))
            print sql_str
            s, f = self.db.get(sql_str)
            if s:
                logger.error(f)
                raise Exception(str(f))
            self.ret['message'] = f
            for i in range(len(self.ret['message'])):
                self.ret['message'][i]['commit_time'] = self.ret['message'][i]['commit_time'].strftime('%Y-%m-%d %H:%M:%S')
            print self.ret
        except Exception, e:
            logger.error(str(e))
            self.ret["status"] = -400
            self.ret["message"] = str(e)
        finally:
            return self.ret

class tag_url(restful.Resource):
    def __init__(self):
        self.ret = {
            "status": 0,
            "message": ""
        }
        self.db = Mydb()

    def get(self, project, domain,  branch, role, tag):
        try:
            sql_str = 'SELECT download_url, config_url FROM tag WHERE ' \
                      'project="%s" AND domain="%s" AND branch="%s" AND role="%s" AND tag="%s"' %(
                      project, domain, branch, role, tag)
            print sql_str
            s, f = self.db.get(sql_str)
            if s:
                logger.error(f)
                raise Exception(str(f))
            self.ret['message'] = f
            print self.ret
        except Exception, e:
            logger.error(str(e))
            self.ret["status"] = -400
            self.ret["message"] = str(e)
        finally:
            return self.ret