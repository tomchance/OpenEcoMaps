# -*- coding: utf-8 -*-
#! /usr/bin/python

"""
  kml_processing.py
  Copyright 2010-13 Tom Chance <tom@acrewoods.net>

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

__author__ = "Tom Chance"
__email__ = "tom@acrewoods.net"
__copyright__ = "Copyright 2010-13, Tom Chance"
__license__ = "GPL"

import flickr
import re
import sys

def generateKMLStyle(name,icon):
  """
    Return a valid KML style definition
  """
  return """<Style id="%s">\n\t<IconStyle>\n\t\t<Icon>\n\t\t\t<href>http://www.openecomaps.co.uk/feature_icons/%s</href>\n\t\t</Icon>\n\t\t<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>\n\t</IconStyle>\n</Style>\n""" % (name,icon)

def generateKMLHeader(styles,document_name):
  """
    Return a valid KML header definition
  """
  kml_styles = ''
  for name,icon in styles.iteritems():
    kml_styles = ''.join([kml_styles, generateKMLStyle(name,icon)])
  return """<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n\t<name>%s</name>\n%s\n\n""" % (document_name, kml_styles)

def generateKMLPlacemark(row):
  """
    Return a valid KML placemark definition adding in
    data from the universal tags (description, website, etc.)
  """
  try:
    test = row['popup_title'].decode('ascii')
    title = row['popup_title']
  except UnicodeEncodeError:
    title = row['popup_title'].encode('ascii', 'xmlcharrefreplace')
  lon = row['lon']
  lat = row['lat']
  popupContents = ''
  cycle_link = "http://www.cyclestreets.net/journey/to/%s,%s,15/" % (lat, lon)
  walk_link = "http://maps.cloudmade.com/?lat=%s&lng=%s&zoom=15&directions=%s,%s&travel=foot&styleId=27911&opened_tab=1" % (lat, lon, lat, lon)
  travel_to_links = "<div class=\"travel\"><a href=\"%s\" target=\"_blank\"><img src=\"http://www.openecomaps.co.uk/images/cyclehere.png\" width=\"55\" height=\"45\" alt=\"Cycle here\" /></a> <a href=\"%s\" target=\"_blank\"><img src=\"http://www.openecomaps.co.uk/images/walkhere.png\" width=\"55\" height=\"45\" alt=\"Walk here\" /></a></div>" % (cycle_link, walk_link)
  popupContents = "".join([popupContents, travel_to_links])
  if ('popup_contents' in row):
      popupContents = "".join([popupContents, "<p>", u'%s' % (row['popup_contents']), "</p>"])
  if ('flickr' in row):
    try:
      pdata = flickr._doget('flickr.photos.getSizes', photo_id=row['flickr'])
      for psize in pdata.rsp.sizes.size:
        if (psize.label == 'Small'):
          popupContents = "".join([popupContents, """<p><img src="%s"></p>""" % (psize.source)])
    except:
      pass
  if ('operator' in row):
    popupContents = "".join([popupContents, """<p><strong>Operator:</strong> %s</p>""" % (row['operator'])])
  if ('website' in row or 'wikipedia' in row):
    popupContents = "".join([popupContents, "<p><strong>More information:</strong> "])
    if ('website' in row):
      popupContents = "".join([popupContents, """<a href="%s">Website</a> """ % (row['website'])])
    if ('wikipedia' in row):
      row['wikipedia'] = re.sub(r'en:', '', row['wikipedia'])
      row['wikipedia'] = re.sub(r'http://en.wikipedia.org/wiki/', '', row['wikipedia'])
      popupContents = "".join([popupContents, """<a href="http://en.wikipedia.org/wiki/%s">Wikipedia article</a>""" % (row['wikipedia'])])
    popupContents = "".join([popupContents, "</p>"])
  return """<Placemark>\n\t<name>%s</name>\n\t<description><![CDATA[%s]]></description>\n\t<styleUrl>#%s</styleUrl>\n\t<Point>\n\t\t<coordinates>%s,%s</coordinates>\n\t</Point>\n</Placemark>\n""" % (title,popupContents,row['popup_style'],lon,lat)

def createKMLFile(title, output, filename, styles):
  """
  Create a valid KML document for all the features
  downloaded and save to a file
  """
  filename = 'kml/' + filename + '.kml'
  filename = str.lower(filename.replace(' ', '_'))
  if ('-v' in sys.argv):
    print " : Writing to KML « " + filename + " »"
  header = generateKMLHeader(styles, title)
  body = ''
  for feature in output:
    body = ''.join([body, generateKMLPlacemark(feature)])
  output = ''.join([header, body, "</Document></kml>"])
  f = open(filename, 'w')
  try:
    test = output.decode('ascii')
  except UnicodeEncodeError:
    output = output.encode('ascii', 'xmlcharrefreplace')
  f.write(output)
  f.close()
