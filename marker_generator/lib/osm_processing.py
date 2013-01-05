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

try: import simplejson as json
except ImportError: import json
import urllib2
import sys

def escape(html):
    """
      Returns the given HTML with ampersands, quotes and carets encoded.
    """
    return html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')


def processRawData(key, value, bbox, server):
  """
  Downloads all nodes, ways and relations with the key/value pair from the Overpass server
  """
  query = """interpreter?data=[out:json];(node(%s)["%s"="%s"];(relation(%s)["%s"="%s"];node(r)->.nodes;way(r);node(w););(way(%s)["%s"="%s"];node(w);););out;""" % (bbox, key, value, bbox, key, value, bbox, key, value)
  f = urllib2.urlopen(server + query)
  data = json.load(f)
  if ('-v' in sys.argv):
    print " : Downloading %s=%s « %s »" % (key, value, server + query)

  # Indexes for nodes and ways needed to find lat/lon centrepoints for ways and relations
  node_index = {}
  way_index = {}
  
  # The object we will return
  features = []

  if ('-v' in sys.argv):
    print " : Processing data..."
    
  for item in data['elements']:
    # Nodes are simple, add their lat/lon to the index and if it also matches the
    # key/value pair then add to the features object
    if (item['type'] == 'node'):
      node_index[item['id']] = { 'lat' : item['lat'], 'lon' : item['lon'] } 
      if ('tags' in item):
        if (key in item['tags'] and item['tags'][key] == value):
          thisitem = { 'lat' : item['lat'], 'lon' : item['lon'] }
          for tagkey in item['tags'].keys():
            thisitem[tagkey] = escape(item['tags'][tagkey])
          features.append(thisitem)

    # For ways, find centrepoints using node index, add to way index, and if it also matches 
    # the key/value pair then add to the features object
    elif (item['type'] == 'way'):
      lats = []
      lons = []
      for node in item['nodes']:
          lats.append(node_index[node]['lat'])
          lons.append(node_index[node]['lon'])
      latcen = "{0:.4f}".format((max(lats) + min(lats)) / 2)
      loncen = "{0:.4f}".format((max(lons) + min(lons)) / 2)
      way_index[item['id']] = { 'lat' : latcen, 'lon' : loncen }
      if ('tags' in item):
        if (key in item['tags'] and item['tags'][key] == value):
          thisitem = { 'lat' : latcen, 'lon' : loncen }
          for tagkey in item['tags'].keys():
            thisitem[tagkey] = escape(item['tags'][tagkey])
          features.append(thisitem)

    # For relations, find centrepoints of multipolygon outer ways using way index, and 
    # if it also matches the key/value pair then add to the features object
    elif (item['type'] == 'relation'):
      lats = []
      lons = []
      for member in item['members']:
        if ('role' in member):
          if (member['role'] == 'outer'):
            latcen = way_index[member['ref']]['lat']
            loncen = way_index[member['ref']]['lon']
      if ('tags' in item):
        if (key in item['tags'] and item['tags'][key] == value):
          thisitem = { 'lat' : latcen, 'lon' : loncen }
          for tagkey in item['tags'].keys():
            thisitem[tagkey] = escape(item['tags'][tagkey])
          features.append(thisitem)
  
  # Return the goodness
  return features