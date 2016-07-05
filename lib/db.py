#!/usr/bin/env python2.7
#coding=utf-8

import MySQLdb
from lib.logging import create_logger
from app import cfg

logger = create_logger(__name__)

__all__ = ['connect', 'modify', 'get']

class Mydb:
    def __init__(self):
        self._conn, self.cursor = None, None
        self._connect()

    def _connect(self):
        try:
            self._conn = MySQLdb.connect(host=cfg['mysql_host'], db=cfg['mysql_db'], user=cfg['mysql_user'],
                                         passwd=cfg['mysql_pass'], port=cfg['mysql_port'], charset='utf8')

            self.cursor = self._conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

        except Exception, e:
            self.msg = 'Error when connect mysql: %s' % e.args
            logger.error(self.msg)

    def connect(self):
        try:
            if not self.conn.ping():
                logger.debug('Reconnect mysql...')
                self._connect()
        except Exception:
            logger.debug('Reconnect mysql...')
            self._connect()

    def get(self, sql):
        self.connect()
        print sql
        try:
            self.cursor.execute(sql)
            raw_records = self.cursor.fetchall()
            return 0, list(raw_records)
        except Exception, e:
            logger.error(e.args)
            return 1, []
        finally:
            self.cursor.close()

    def modify(self, sql):
        self.connect()
        try:
            self.cursor.execute(sql)
            c = self._conn.commit()
            return 0, c
        except Exception, e:
            logger.error(e.args)
            return 2, 'sql error'
        finally:
            self.cursor.close()

    def disconnect_db(self):
        if self.conn.ping():
            self.conn.close()
            self.conn = None