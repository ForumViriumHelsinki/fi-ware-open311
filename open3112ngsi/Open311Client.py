# -*- coding: utf-8 -*-
#
# Part of Open311-NGSI integration tool
# (c) 2014, Juho Vuori
#
# http://www.forumvirium.fi/
#

import ssl
import json
from three import Three

SSL_PROTOCOL = {'ssl_version': ssl.PROTOCOL_TLSv1}
''' Open 311 endpoint URL '''
OPEN_311_URL = 'http://asiointi.hel.fi/palautews/rest/v1/'

def getOpen311Services():
    t = Three(OPEN_311_URL, ssl_version=ssl.PROTOCOL_TLSv1)
    services = t.services()
    return services

def getOpen311Discovery():
    t = Three(OPEN_311_URL, ssl_version=ssl.PROTOCOL_TLSv1)
    print t.discovery()

def getOpen311Request(requestId):
    t = Three(OPEN_311_URL, ssl_version=ssl.PROTOCOL_TLSv1)
    a= t.requests(service_request_id=requestId)
    return a

def getOpen311Requests(since,until):
    t = Three(OPEN_311_URL, ssl_version=ssl.PROTOCOL_TLSv1)
    start = since is not None and '%02d-%02d-%02d' %(since.month,since.day,since.year) or None
    end = until is not None and '%02d-%02d-%02d' %(until.month,until.day,until.year) or None
    return t.requests(start=start,end=end,extensions=True)

