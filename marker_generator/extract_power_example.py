# -*- coding: utf-8 -*-
#! /usr/bin/python

"""
  osm_processing.py
  Copyright 2010-13 Tom Chance <tom@acrewoods.net>

  Functions to download data from OpenStreetMap and turn it into
  a Python dictionary

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

__author__ = "Tom Chance"
__email__ = "tom@acrewoods.net"
__copyright__ = "Copyright 2010-13, Tom Chance"
__license__ = "GPL"

import os
import sys
from lib.feature_defs import *
from lib.kml_processing import *
from lib.geojson_processing import *

from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('settings.cfg')

def doTheJob(bbox, filename, features, title):
  if ('-v' in sys.argv):
    print title
  features_list = features.split(';')
  for feature in features_list:
    function = "feature_%s" % (feature)
    output, styles = globals()[function](bbox, {}, parser.get('overpass', 'server'))
    createJSONFile(title, output, filename, styles)
    createKMLFile(title, output, filename, styles)

if __name__=="__main__":
  doTheJob('51.20,-0.51,51.80,0.35', 'power', 'powergenerator', 'Low carbon power in London')