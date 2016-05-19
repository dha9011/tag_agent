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

def url_is_correct(url):
    if re.match(r'^https?:/{2}.*?$', url):
        return True
    else:
        return False

class tag_submit(restful.Resource):
    def __init__(self):
        self.ret = {
            "status": "0",
            "message": ""
        }
        self.db = Mydb()

    def post(self):
        #判断post的值是否正确
        arguments = [
            Arg('tag', type=str, required=True, help='Miss tag'),
            Arg('domain', type=str, required=True, help='Miss domain'),
            Arg('project', type=str, required=True, help='Miss project'),
            Arg('role', type=str, required=True, help='Miss role'),
            Arg('comment', type=str, required=True, help='Miss comment'),
            Arg('commit_time', type=str, required=True, help='Miss commit_time'),
            Arg('commit_user', type=str, required=True, help='Miss commit_user'),
            Arg('download_url', type=str, required=True, help='Miss download_url'),
            Arg('config_url', type=str, required=True, help='Miss config_url'),
            Arg('is_ready', type=str, required=True, help='Miss is_ready'),
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
        if not(url_is_correct(tag_config_url) and url_is_correct(tag_download_url)):
            self.ret["status"] = "-7"
            self.ret["message"] = "invalid config or download url"
            return self.ret
        tag_is_ready = args['is_ready']
        #判断此tag值是否已经存在
        sql_str = 'SELECT tag FROM tag WHERE tag="%s" and project="%s" and role="%s"' % (
                    tag_tag, tag_project, tag_role)
        exist_tag = self.db.get(sql_str)["message"]
        if exist_tag:
            self.ret["status"] = "-9"
            self.ret["message"] = "tag is exist"
            return self.ret
        ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
        try:
            #将提交时间的字符转转化成datetime格式
            tag_commit_time = datetime.datetime.strptime(tag_commit_time, ISOTIMEFORMAT)
        except Exception, e:
            self.ret["status"] = "-1"
            self.ret["message"] = e.args
            return self.ret
        print tag_commit_time
        sql_str = 'INSERT INTO tag (tag, domain, project, role, comment, commit_time, commit_user, config_url, download_url, is_ready) ' \
                  'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        params = [tag_tag, tag_domain, tag_project, tag_role, tag_comment, tag_commit_time, tag_commit_user, tag_config_url, tag_download_url, tag_is_ready]
        print params
        self.ret = self.db.modify(sql_str, params)
        if self.ret["status"] != "0":
            logger.error(self.ret["message"])
            return self.ret
        logger.info('insert a tag info: %s', self.ret["message"])
        return self.ret

class tag_list(restful.Resource):
    def __init__(self):
        self.ret = {
            "status" : "0",
            "message": ""
        }
        self.db = Mydb()

    def get(self, project, domain, role):
        tag_project = project
        tag_domain = domain
        tag_role = role
        tag_limit = request.args.get('limit')
        if (tag_limit is None) and (tag_limit.isdigit()):
            self.ret["status"] = "-8"
            self.ret["message"] = "Miss limit or limit is not a digit"
            return self.ret
        sql_str = 'SELECT tag,comment, commit_time,commit_user FROM tag ' \
                  'WHERE project="%s" and domain="%s" and role="%s" ORDER BY commit_time DESC LIMIT %d' % (
                   tag_project, tag_domain, tag_role, int(tag_limit))
        print sql_str
        mes = self.db.get(sql_str)["message"]
        self.ret["message"] = []
        #将数据库取出的信息转化成字典
        for item in mes:
            item_dict = {
                'tag'           : item[0],
                'comment'       : item[1],
                'commit_time'   : item[2].strftime('%Y-%m-%d %H:%M:%S'),
                'commit_user'   : item[3]
            }
            self.ret["message"].append(item_dict)
        if self.ret["status"] != "0":
            logger.error(self.ret["message"])
            return self.ret
        logger.info('get tags info: %s', self.ret["message"])
        return self.ret

class tag_url(restful.Resource):
    def __init__(self):
        self.ret = {
            "status": "0",
            "message": ""
        }
        self.db = Mydb()

    def get(self, project, domain, role, tag):
        tag_project = project
        tag_domain = domain
        tag_role = role
        tag_tag = tag
        sql_str = 'SELECT download_url, config_url FROM tag WHERE ' \
                  'project="%s" and domain="%s" and role="%s" and tag="%s"' %(
                  tag_project, tag_domain, tag_role, tag_tag)
        url = self.db.get(sql_str)["message"]
        if not url:
            self.ret["status"] = "-9"
            self.ret["message"] = "can't find the tag"
            return self.ret
        else:
            self.ret["message"] = {
                "download_url" : url[0][0],
                "config_url"   : url[0][1]
            }
        if self.ret["status"] != "0":
            logger.error(self.ret["message"])
            return self.ret
        return self.ret
