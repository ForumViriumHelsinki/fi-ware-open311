#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Part of Open311-NGSI integration tool
# (c) 2014, Juho Vuori
#
# http://www.forumvirium.fi/
#


import NGSIClient
import sys

result = NGSIClient.getContextIds('Open311')
d = result.json()
responses = d['contextResponses']
for r in responses:
    print r['contextElement']['id']


