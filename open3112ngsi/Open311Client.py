# -*- coding: utf-8 -*-
#
# Part of Open311-NGSI integration tool
# Author: Juho Vuori (juho.vuori@codento.com)
# Copyright: Forum Virium Helsinki
#
# http://www.forumvirium.fi/
#

import ssl
import json
from three import Three
from config import open311URL

SSL_PROTOCOL = {'ssl_version': ssl.PROTOCOL_TLSv1}

def getOpen311Services():
    t = Three(open311URL, ssl_version=ssl.PROTOCOL_TLSv1)
    services = t.services()
    return services

def getOpen311Discovery():
    t = Three(open311URL, ssl_version=ssl.PROTOCOL_TLSv1)
    print t.discovery()

def getOpen311Request(requestId):
    t = Three(open311URL, ssl_version=ssl.PROTOCOL_TLSv1)
    a= t.requests(service_request_id=requestId)
    return a

def getOpen311Requests(since,until):
    t = Three(open311URL, ssl_version=ssl.PROTOCOL_TLSv1)
    start = since is not None and '%02d-%02d-%02d' %(since.month,since.day,since.year) or None
    end = until is not None and '%02d-%02d-%02d' %(until.month,until.day,until.year) or None
    return t.requests(start=start,end=end,extensions=True)

