#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 17/2/16 PM4:02
# Copyright: TradeShift.com
__author__ = 'liming'

from app import app, api
import resource

RESOURCES = [
    (resource.tag_submit, '/tag/submit'),
    (resource.tag_list, '/tag/list/<string:project>/<string:domain>/<string:role>/<string:branch>'),
    (resource.tag_url, '/tag/url/<string:project>/<string:domain>/<string:role>/<string:branch>/<string:tag>'),
    (resource.branch_list, '/branch/<string:project>/<string:domain>/<string:role>')
]

for res, uri in RESOURCES:
    api.add_resource(res, uri)