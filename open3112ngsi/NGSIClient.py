# -*- coding: utf-8 -*-
#
# Part of Open311-NGSI integration tool
# Author: Juho Vuori (juho.vuori@codento.com)
# Copyright: Forum Virium Helsinki
#
# http://www.forumvirium.fi/
#

import json
import requests
from lxml import etree
from config import orionContextBrokerURL

def makeOrionRequest(urlSuffix,data):
    url = orionContextBrokerURL + urlSuffix
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json"
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)

    return r

def deleteOpen311Context(type, id):
    body = {
        "contextElements" : [
            {
                "type": type,
                "isPattern": "false",
                "id": id,
            }
        ],
        "updateAction": "DELETE"
    }
    return makeOrionRequest("NGSI10/updateContext",body)

def createOpen311Context(type, id, attributes):
    body = {
        "contextElements" : [
            {
                "type": type,
                "isPattern": "false",
                "id": id,
                "attributes": attributes
            }
        ],
        "updateAction": "UPDATE"
    }
    return makeOrionRequest("NGSI10/updateContext",body)

def createOpen311ContextInXML(__type, id, attributes):
    # Orion Context Broker breaks with non-ASCII data in JSON, so we update with XML
    xml = etree.Element('updateContextRequest')
    cel = etree.Element('contextElementList')
    xml.append(cel)
    ce = etree.Element('contextElement')
    cel.append(ce)
    ei = etree.Element('entityId',type=__type,isPattern="false")
    ce.append(ei)
    _id = etree.Element('id')
    ei.append(_id)
    _id.text=id
    cal = etree.Element('contextAttributeList')
    ce.append(cal)
    for attr in attributes:
        ca = etree.Element('contextAttribute')
        cal.append(ca)
        name = etree.Element('name')
        name.text=attr['name']
        ca.append(name)
        _type = etree.Element('type')
        _type.text = attr['type']
        ca.append(_type)
        cv = etree.Element('contextValue')
        value = attr['value']
        cv.text = value
        ca.append(cv)
    up = etree.Element('updateAction')
    up.text = 'APPEND'
    xml.append(up)

    url = orionContextBrokerURL + "NGSI10/updateContext"
    headers = {
        "Accept": "application/json",
        "Content-type": "application/xml"
    }
    r = requests.post(url, data=etree.tostring(xml,encoding="utf-8"), headers=headers)

    return r



def getContextIds(type):
    body = {
        "entities": [
            {
                "type": type,
                "isPattern": "true",
                "id": ".*"
            }
        ],
        "attributes" : [
            "status" # empty attributes list doesn't work...
        ]
    }
    # limit 1000 is maximum allowed
    return makeOrionRequest("NGSI10/queryContext?limit=1000",body)
    
def getContext(type, id):
    body = {
        "entities" : [
            {
                "type": type,
                "isPattern": "false",
                "id": id
            }
        ]
    }
    return makeOrionRequest("NGSI10/queryContext",body)

def getContextNear(type, lat, lng, radius):
    body = {
        "entities": [
            {
                "type": type,
                "isPattern": "true",
                "id": ".*"
            }
        ],
        "restriction": {
            "scopes": [
                {
                    "type" : "FIWARE_Location",
                    "value" : {
                        "circle": {
                            "centerLatitude": str(lat),
                            "centerLongitude": str(lng),
                            "radius": str(radius)
                        }
                    }
                }
            ]
        }
    }
    
    return makeOrionRequest("NGSI10/queryContext",body)


def createOpen311Entity(open311request):
    def safeString(s):
      # Orion context broker has a broken JSON encoder. Everything breaks if we put newlines in there
      # so we just strip them for now. This is wrong, but I can't come up with a better workaround.
      return "".join([x for x in s if x != '\n'])

    def createAttribute(destinationAttribute,sourceAttribute=None,t="string",source=open311request):
        if sourceAttribute is None: sourceAttribute = destinationAttribute
        if source.has_key(sourceAttribute): return {
            "name": destinationAttribute,
            "type": t,
            "value": safeString(source[sourceAttribute])
        }
        else: return None

    def createExtendedAttribute(destinationAttribute,sourceAttribute=None,t="string"):
        if open311request.has_key("extended_attributes"):
            return createAttribute(destinationAttribute,sourceAttribute,t,open311request["extended_attributes"])
        else:
            return None

    def createPositionAttribute(destinationAttribute,sourceLng,sourceLat,t="coords"):
        if open311request.has_key(sourceLat) and open311request.has_key(sourceLng): return {
            "name": destinationAttribute,
            "type": t,
            "value": str(open311request[sourceLng])+','+ str(open311request[sourceLat]),
            "metadatas": [ {"name": "location", "type": "string", "value": "WSG84"} ]
        }
        else: return None
    
    open311entity = [
        createAttribute("service_request_id"), #unique id
        createAttribute("status_notes"), #exlanation of why status was changed
        createAttribute("status"), # open/closed
        createAttribute("service_code",t="integer"), #service request type
        createAttribute("service_name"), #human readable service request type
        createAttribute("description"),
        createAttribute("agency_responsible"),
        createAttribute("service_notice"),
        createAttribute("requested_datetime",t="datetime"),
        createAttribute("updated_datetime",t="datetime"),
        createAttribute("expected_datetime",t="datetime"),
        createAttribute("address",t="address"),
        createAttribute("media_url",t="url"),
        createPositionAttribute("position","long","lat"),
        createExtendedAttribute("service_object_id",t="integer"),
        createExtendedAttribute("service_object_type",t="url"),
        createExtendedAttribute("title"),
        createExtendedAttribute("detailed_status"),
    ]
    return [x for x in open311entity if x is not None]


