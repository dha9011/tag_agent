#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 17/2/16 PM4:02
# Copyright: TradeShift.com
__author__ = 'liming'

from app import app, api
import resource

RESOURCES = [
    (resource.tag_submit, '/tag/submit'),
    (resource.tag_list, '/tag/<string:project>/<string:domain>/<string:role>'),
    (resource.tag_url, '/tag/<string:project>/<string:domain>/<string:role>/<string:tag>')
]

for res, uri in RESOURCES:
    api.add_resource(res, uri)