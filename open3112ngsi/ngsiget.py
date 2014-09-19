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

for arg in sys.argv[1:]:
  print arg
  result = NGSIClient.getContext('Open311', arg)
  print result.json()

if len(sys.argv) < 2:
  print "give id" #   '39lig11fhtpgbafkmqol'

