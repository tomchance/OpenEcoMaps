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
from lib.kml_processing import *
from lib.feature_defs import * 

bbox_london = '-0.51,51.20,0.35,51.80'
bbox_uk = '-6.5,49.68,2.67,61.31'

def createKML(bbox, features, myStyles):
  """
  Grab the raw data, process it and call the required feature_* functions
  to create the KML
  """
  output = ""
  for feature in features:
    featurekey = feature.keys()[0]
    featurevalue = feature[featurekey]
    if ('-v' in sys.argv):
      print ''.join([featurekey, "=", featurevalue])
    function = "feature_%s%s" % (featurekey, featurevalue)
    this_output, myStyles = globals()[function](bbox, myStyles)
    output = ''.join([output, this_output])
  return output, myStyles

def createKMLFile(title, contents, filename, myStyles):
  """
  Sandwich the contents in a KML header and footer, and dump it into
  a file
  """
  header = generateKMLHeader(myStyles, title)
  output = ''.join([header, contents, "</Document></kml>"])
  f = open(filename, 'w')
  f.write(output)
  f.close()

def doTheJob(bbox, filename, features, title):
  feature_contents, myStyles = createKML(bbox, features, {})
  createKMLFile(title, feature_contents, filename, myStyles)

if __name__=="__main__":
  doTheJob(bbox_london, 'kml/london/power.kml', [{'power':'generator'}], 'Low carbon power generators in London')
  doTheJob(bbox_uk, 'kml/uk/power.kml', [{'power':'generator'}], 'Low carbon power generators in the UK')
  doTheJob(bbox_london, 'kml/london/waste.kml', [{'amenity':'recycling'}, {'amenity':'waste_transfer_station'}, {'landuse':'landfill'}], 'Zero waste in London')
  doTheJob(bbox_london, 'kml/london/transport.kml', [{'railway':'station'}, {'amenity':'bicycle_rental'}, {'amenity':'car_sharing'}, {'railway':'tram_stop'}], 'Sustainable transport in London')
  doTheJob(bbox_london, 'kml/london/food.kml', [{'amenity':'marketplace'}, {'landuse':'allotments'}], 'Sustainable food in London')
  doTheJob(bbox_london, 'kml/london/culture.kml', [{'amenity':'library'}, {'amenity':'theatre'}, {'amenity':'cinema'}, {'tourism':'gallery'}, {'tourism':'museum'}], 'Culture and heritage in London')
