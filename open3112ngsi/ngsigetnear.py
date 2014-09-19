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

if len(sys.argv) == 4:
  lat = sys.argv[1]
  lng = sys.argv[2]
  radius = sys.argv[3]
  result = NGSIClient.getContextNear('Open311', lat, lng, radius)
  try:
      print result.json()
  except:
      print "Invalid json "

else:
  print "usage: ngsigetnear lat lng radius" #   '39lig11fhtpgbafkmqol'

