#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Part of Open311-NGSI integration tool
# Author: Juho Vuori (juho.vuori@codento.com)
# Copyright: Forum Virium Helsinki
#
# http://www.forumvirium.fi/
#

"""open3112ngsi.py

Usage:
  open3112ngsi.py [options] truncate
  open3112ngsi.py [options] all
  open3112ngsi.py [options] id <id>
  open3112ngsi.py [options] file <file>
  open3112ngsi.py [options] between <begin> <end>
  open3112ngsi.py [options] since-last-update

Options:
  -o <file>     Output to file.
  -h --help     Show this screen.
  --version     Show version.
"""


import sys
from datetime import datetime,timedelta
import simplejson as json
import Open311Client
import NGSIClient
from docopt import docopt

def truncateNGSI():
    #NGSIClient.deleteOpen311Context("Open311", request['service_request_id'])
    pass

def toDateTime(s):
    return datetime.strptime(s,'%Y-%m-%d')

def getAllRequests():
    # There is no reliable method to get all requests from Open311 API. We just loop through all days
    # since a known fixed begin date
    end = datetime.now()
    current = datetime(2014,6,10,0,0,0)
    while current < end:
        next = current + timedelta(1)
        print "reading requests between %s and %s" % (current,next)
        block = Open311Client.getOpen311Requests(current,next)
        print "%d requests" % (len(block))
        for item in block:
            yield item
        current = next

def requestsIntoNGSI(requests):
    for request in requests:
        entity = NGSIClient.createOpen311Entity(request)
        id = request['service_request_id']
        #print open311request
        print id
        print entity
        NGSIClient.createOpen311ContextInXML("Open311", id, entity)

if __name__ == "__main__":
    arguments = docopt(__doc__, version='1.0')

    if arguments['truncate']:
        truncateNGSI()
    else:
        if arguments['all']:
            requests = getAllRequests()
        elif arguments['file']:
            fn = arguments['<file>']
            if fn == '-': f = sys.stdin
            else: f = open(fn,"r")
            data = "\n".join(f.readlines())
            requests = json.loads(data)
        elif arguments['id']:
            requests = Open311Client.getOpen311Request(arguments['<id>'])
        elif arguments['between']:
            requests = Open311Client.getOpen311Requests(toDateTime(arguments['<begin>']),toDateTime(arguments['<end>']))
        elif arguments['since-last-update']:
            requests = Open311Client.getOpen311Requests(figureOutLastUpdate(),None)
        else: raise Exception()
        if arguments["-o"]:
            fn = arguments['-o']
            if fn == '-': f = sys.stdout
            else: f = open(fn,"w")
            converted = [x for x in requests]
            f.write(json.dumps(converted))
        else:
            requestsIntoNGSI(requests)

