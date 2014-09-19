#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Part of Open311-NGSI integration tool
# Author: Juho Vuori (juho.vuori@codento.com)
# Copyright: Forum Virium Helsinki
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


