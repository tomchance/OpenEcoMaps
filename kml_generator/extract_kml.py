# -*- coding: utf-8 -*-
#! /usr/bin/python

"""
  extract_kml.py
  Copyright 2010-11 Tom Chance <tom@acrewoods.net>

  This script downloads data from OpenStreetMap related to
  sustainable lifemyStyles and turns it into KML feeds.

  This program is free software; you may redistribute it and/or
  modify it under the terms of the GNU General Public License as
  published by the Free Software Foundation; either version 3 of
  the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful, 
  but WITHOUT ANY WARRANTY; without even the implied warranty of 
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
  GNU General Public License for more details.

  http://www.gnu.org/licenses/gpl-3.0.html
"""

import os
import sys
sys.path.append('./lib')
from kml_processing import *
from feature_defs import *

def createKML(bbox, title, features):
  """
  Grab the raw data, process it and call the required feature_* functions
  to create the KML
  """
  myStyles = {}
  output = ""
  for featurekey,featurevalue in features.iteritems():
    function = "feature_%s%s" % (featurekey, featurevalue)
    print function
    this_output, myStyles = globals()[function](bbox, myStyles)
    output = ''.join([output, this_output])
  header = generateKMLHeader(myStyles, title)
  output = ''.join([header, output, "</Document></kml>"])
  return output

#do power for london...
  #given this bbox
  #this title
  #this list of features
  #dump into this KML file

bbox = '-0.1028,51.4446,-0.0487,51.4731'
title = 'Allotments in East Dulwich-ish'
features = {'landuse':'allotments', 'amenity':'recycling'}
results = createKML(bbox, title, features)
print results