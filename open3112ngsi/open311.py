# -*- coding: utf-8 -*-
#
# Part of Open311-NGSI integration tool
# (c) 2014, Juho Vuori
#
# http://www.forumvirium.fi/
#

import requests
import json
import ssl
from requests.adapters import HTTPAdapter

OPEN_311_BASE_URL = 'http://asiointi.hel.fi/palautews/rest/v1/'

class SSLAdapter(HTTPAdapter):
    '''An HTTPS Transport Adapter that uses an arbitrary SSL version.'''
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version

        super(SSLAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=self.ssl_version)

class Open311Importer():

    def setup(self):
        self.authenticate()

    def authenticate(self):
       '''
       This needs to be implemented only in case there write operations to the API is needed
       '''
    
    def get_services(self, service_code=None, **kwargs):
       ''' 
       Get available services in this Open311 endpoint
       '''
#    self.get_service()
    
    def get_services(self, *args, **kwargs):
        """
        Send a request to Open311 endpoint to fetch service data
        """ 
        url = OPEN_311_BASE_URL + 'services.json'
        print url
        content = requests.get(url).json()
        return content 

self.session.mount('https://', SSLAdapter('ssl.PROTOCOL_TLSv1'))
o = Open311Importer()
response = o.get_services()
print (response)
