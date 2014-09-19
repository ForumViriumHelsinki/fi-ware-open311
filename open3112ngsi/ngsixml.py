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

for arg in sys.argv[1:]:
  print arg
  result = NGSIClient.getContext('Open311', arg, True)
  rr = NGSIClient.createOpen311XML()
  print rr

  import pdb;pdb.set_trace()

  print result.text

if len(sys.argv) < 2:
  print "give id" #   '39lig11fhtpgbafkmqol'

