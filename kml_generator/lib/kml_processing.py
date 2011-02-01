# -*- coding: utf-8 -*-
#! /usr/bin/python

"""
  kml_processing.py
  Copyright 2010-11 Tom Chance <tom@acrewoods.net>

  Functions to create KML files

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

import flickr
import re
import sys

__author__ = "Tom Chance"
__email__ = "tom@acrewoods.net"
__copyright__ = "Copyright 2010-11, Tom Chance"
__license__ = "GPL"

def generateKMLStyle(name,icon):
  """
    Return a valid KML style definition
  """
  return """<Style id="%s">\n\t<IconStyle>\n\t\t<Icon>\n\t\t\t<href>http://www.openecomaps.co.uk/feature_icons/%s</href>\n\t\t</Icon>\n\t\t<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>\n\t</IconStyle>\n</Style>\n""" % (name,icon)

def generateKMLHeader(styles,document_name):
  """
    Return a valud KML header definition
  """
  kml_styles = ''
  for name,icon in styles.iteritems():
    kml_styles = ''.join([kml_styles, generateKMLStyle(name,icon)])
  return """<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n\t<name>%s</name>\n%s\n\n""" % (document_name, kml_styles)

def generateKMLPlacemark(row,style):
  """
    Return a valud KML placemark definition adding in
    data from the universal tags (description, website, etc.)
  """
  name = u'%s' % (row['name'].decode('utf-8'))
  name = name.encode('ascii', 'xmlcharrefreplace')
  lon = row['lon']
  lat = row['lat']
  if (row['description']):
    description = u'%s' % (row['description'])
  else:
    description = "<p>No further details known</p>"
  if (row['flickr']):
    pdata = flickr._doget('flickr.photos.getSizes', photo_id=row['flickr'])
    for psize in pdata.rsp.sizes.size:
      if (psize.label == 'Small'):
        description = "".join([description, """<p><img src="%s"></p>""" % (psize.source)])
  if (row['operator']):
    description = "".join([description, """<p><strong>Operator:</strong> %s</p>""" % (row['operator'])])
  if (row['website'] or row['wikipedia']):
    description = "".join([description, "<p><strong>More information:</strong> "])
    if (row['website']):
      description = "".join([description, """<a href="%s">Website</a> """ % (row['website'])])
    if (row['wikipedia']):
      row['wikipedia'] = re.sub(r'en:', '', row['wikipedia'])
      row['wikipedia'] = re.sub(r'http://en.wikipedia.org/wiki/', '', row['wikipedia'])
      description = "".join([description, """<a href="http://en.wikipedia.org/wiki/%s">Wikipedia article</a>""" % (row['wikipedia'])])
    description = "".join([description, "</p>"])
  return """<Placemark>\n\t<name>%s</name>\n\t<description><![CDATA[%s]]></description>\n\t<styleUrl>#%s</styleUrl>\n\t<Point>\n\t\t<coordinates>%s,%s</coordinates>\n\t</Point>\n</Placemark>\n""" % (name,description,style,lon,lat)
