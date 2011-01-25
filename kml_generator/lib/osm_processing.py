# -*- coding: utf-8 -*-
#! /usr/bin/python

"""
  osm_processing.py
  Copyright 2010-11 Tom Chance <tom@acrewoods.net>

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

import sys
import csv
import urllib
import libxslt
import libxml2
libxml2.lineNumbersDefault(1)
libxml2.substituteEntitiesDefault(1)

def escape(html):
    """
      Returns the given HTML with ampersands, quotes and carets encoded.
    """
    return html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')


def processRawData(xsl_uri, features, bbox):
  """
    Downloads the data from XAPI and turns it into a Python object.
  """
  # Download data to temporary file and read the XML/XSL into memory
  for key,value in features.iteritems():
    xapi_fragment = "%s=%s" % (key,value)
  xapi_uri = "http://xapi.openstreetmap.org/api/0.6/*[%s][bbox=%s]" % (xapi_fragment, bbox)
  xsl_uri = ''.join(['./lib/', xsl_uri])
  if ('-v' in sys.argv):
    print " : Downloading %s" % (xapi_uri)
  urllib.urlretrieve(xapi_uri,'temp.xml')
  osmdoc = libxml2.parseFile('temp.xml')
  styledoc = libxml2.parseFile(xsl_uri)
  style = libxslt.parseStylesheetDoc(styledoc)

  # Translate XML to CSV (easier to then read into py object)
  if ('-v' in sys.argv):
    print " : Processing data..."
  for key,value in features.iteritems():
    result = style.applyStylesheet(osmdoc,\
      { "key":"'%s'"%key, "value":"'%s'"%value })
    style.saveResultToFilename('temp.csv', result, 0)

  # Encode HTML elements
  f = open('temp.csv', 'r')
  safe_content = escape(f.read())
  f = open('temp.csv', 'w')
  f.write(safe_content)
  
  # Read CSV file into dict
  pdata = csv.DictReader(open('temp.csv', 'rb'), delimiter='	')
  return pdata
