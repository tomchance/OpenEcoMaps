# -*- coding: utf-8 -*-
#! /usr/bin/python

'''
extract_kml.py
Copyright 2010-13, Tom Chance <tom@acrewoods.net>

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
'''

__author__ = 'Tom Chance'
__email__ = 'tom@acrewoods.net'
__copyright__ = 'Copyright 2010-13, Tom Chance'
__license__ = 'GPL'

import os
import sys
import MySQLdb
from lib.feature_defs import *
from lib.kml_processing import *
from lib.geojson_processing import *

from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('settings.cfg')
DBHOST = parser.get('database', 'host')
DBUSER = parser.get('database', 'user')
DBPASSWD = parser.get('database', 'passwd')
DBDB = parser.get('database', 'db')
OVERPASS = parser.get('overpass', 'server')

def doTheJob(bbox, filename, packtitle, features, layername):
  if ('-v' in sys.argv):
    print ''.join([packtitle, ' --> ', layername, ' (', filename, ')'])
  features_list = features.split(';')
  for feature in features_list:
    function = "feature_%s" % (feature)
    output, styles = globals()[function](bbox, {}, parser.get('overpass', 'server'))
    createJSONFile(layername, output, filename, styles)
    createKMLFile(layername, output, filename, styles)

if __name__=='__main__':
  db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASSWD, db=DBDB)
  cursor = db.cursor()
  cursor.execute('SELECT packs.bbox, packs.title, layers.features, layers.name from packs, layers, pack_layers WHERE pack_layers.layer = layers.id AND pack_layers.pack = packs.id')
  layers = cursor.fetchall()
  for layer in layers:
    filename = ''.join([layer[1], '/', layer[3]])
    try:
      doTheJob(layer[0], filename, layer[1], layer[2], layer[3])
    except:
     if ('-v' in sys.argv):
       print '*** Blast, that layer failed. I tried %s on bbox %s to no avail. Moving on... ***' % (layer[2], layer[0])
