#!/usr/bin/env python2.7
#coding=utf-8

import MySQLdb
from lib.logging import create_logger
logger = create_logger(__name__)

class Mydb:
    def __init__(self):
        self.username = 'root'
        self.password = '5673914'
        self.db = 'app_tag'
        self.port = 3306
        self.host = 'localhost'
        self.charset = 'utf8'
        self.conn = ''
        self.times = 0


    def connect_db(self):
        try:
            self.conn = MySQLdb.connect(host = self.host, user = self.username, passwd = self.password, db = self.db, port = self.port,
                                        read_default_file = '/etc/my.cnf', charset = self.charset)
        except Exception, e:
            logger.error(e.args)

    def connect(self):
        if self.times > 5:
            logger.warning('connect database failed')
            self.times = 0
            return
        try:
            if not self.conn.ping():
                self.connect_db()
        except:
            self.times += 1
            self.connect_db()

    def modify(self, sql_str,params=None):
        self.connect()
        if sql_str != "":
            try:
                cur = self.conn.cursor()
                cur.execute(sql_str, params)
                self.conn.commit()
                cur.close()
                return {"status": "0", "message": "update data successfully"}
            except Exception, e:
                self.disconnect_db()
                return {"status": "-10", "message": e.args}
        else:
            return {"status": "-1", "message": "no sql command"}

    def get(self,sql_str):
        self.connect()
        if sql_str != "":
            try:
                cur = self.conn.cursor()
                cur.execute(sql_str)
                records = cur.fetchall()
                cur.close()
                return {"status": "0", "message": list(records)}
            except Exception,e:
                return {"status": "-9", "message": e.args}
        else:
            return {"status": "-1", "message": "no sql command"}

    def disconnect_db(self):
        if self.conn.ping():
            self.conn.close()
            self.conn = ''
            self.times = 0