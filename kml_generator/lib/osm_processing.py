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

__author__ = "Tom Chance"
__email__ = "tom@acrewoods.net"
__copyright__ = "Copyright 2010-11, Tom Chance"
__license__ = "GPL"

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
  # Download data to temporary file
  xapi_uri = "http://open.mapquestapi.com/xapi/api/0.6/*[%s][bbox=%s]" % (features, bbox)
  if ('-v' in sys.argv):
    print " : Downloading %s" % (xapi_uri)
  urllib.urlretrieve(xapi_uri,'temp.xml')
  
  # Translate XML to CSV (easier to then read into py object)
  if ('-v' in sys.argv):
    print " : Processing data..."
  osmdoc = libxml2.parseFile('temp.xml')
  styledoc = libxml2.parseFile(xsl_uri)
  style = libxslt.parseStylesheetDoc(styledoc)
  result = style.applyStylesheet(osmdoc, None)
  style.saveResultToFilename('temp.csv', result, 0)

  # Encode HTML elements
  f = open('temp.csv', 'r')
  safe_content = escape(f.read())
  f = open('temp.csv', 'w')
  f.write(safe_content)
  
  # Read CSV file into dict
  pdata = csv.DictReader(open('temp.csv', 'rb'), delimiter='	')
  return pdata
