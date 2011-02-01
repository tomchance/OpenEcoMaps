# -*- coding: utf-8 -*-
#! /usr/bin/python

"""
  feature_defs.py
  Copyright 2010-11 Tom Chance <tom@acrewoods.net>

  Functions to define how we process different OpenStreetMap
  features

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

from lib.osm_processing import *
from lib.kml_processing import *
import re
import flickr

def feature_generic(bbox, defaultName, style, features):
  """
    Generic features (no fancy info in the description)
  """
  output = ''
  xsl_uri = 'lib/trans_generic.xsl'
  poi_data = processRawData(xsl_uri, features, bbox)
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if (row['name'] == ''):
      row['name'] = defaultName
    output = ''.join([output, generateKMLPlacemark(row, style)])
  return output
    
def feature_amenitybicycle_rental(bbox, myStyles):
  """
    Bike hire...
  """
  myStyles["transportCyclehire"] = "transport_cyclehire.png"
  xsl_uri = 'lib/trans_generic.xsl'
  features = {"amenity":"bicycle_rental"}
  poi_data = processRawData(xsl_uri, features, bbox)
  output = ''
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if (row['name'] == ''):
      row['name'] = 'Cycle hire docking bay'
    if (row['network'] == 'Barclays Cycle Hire'):
      row['name'] = ''.join(['TfL Cycle Hire: ', row['name']])
    if (row['capacity']):
      row['description'] = ''.join([row['description'], "<p><strong>Capacity:</strong> %s</p>" % (row['capacity'])])
    output = ''.join([output, generateKMLPlacemark(row, "transportCyclehire")])
  return output, myStyles

def feature_amenitycar_sharing(bbox, myStyles):
  """
    Car club parking bays...
  """
  myStyles["transportCarshare"] = "transport_carsharing.png"
  features = {"amenity":"car_sharing"}
  output = feature_generic(bbox, "Car club parking bay", "transportCarshare", features)
  return output, myStyles

def feature_amenitycinema(bbox, myStyles):
  """
    Cinemas...
  """
  myStyles["cultureCinema"] = "culture_cinema.png"
  features = {"amenity":"cinema"}
  output = feature_generic(bbox, "Cinema", "cultureCinema", features)
  return output, myStyles

def feature_amenitylibrary(bbox, myStyles):
  """
    Libraries...
  """
  myStyles["cultureLibrary"] = "culture_library.png"
  features = {"amenity":"library"}
  output = feature_generic(bbox, "Library", "cultureLibrary", features)
  return output, myStyles
    
def feature_amenitymarketplace(bbox, myStyles):
  """
    Food markets...
  """
  myStyles["foodMarket"] = "food_market.png"
  xsl_uri = 'lib/trans_markets.xsl'
  features = {"amenity":"marketplace"}
  poi_data = processRawData(xsl_uri, features, bbox)
  output = ''
  for row in poi_data:
    if (row['lat'] == None):
      continue
    # Skip markets that don't sell fish/meat/veg
    if (row['vegetables'] != 'yes' and row['meat'] != 'yes' and row['fish'] != 'yes'):
      continue
    if (row['name'] == ''):
      row['name'] = 'Food market'
    output = ''.join([output, generateKMLPlacemark(row, 'foodMarket')])
  return output, myStyles
    
def feature_amenityrecycling(bbox, myStyles):
  """
    Recycling bins...
  """
  myStyles["wasteRecyclingBin"] = "waste_recycle.png"
  xsl_uri = 'lib/trans_recycling.xsl'
  features = {"amenity":"recycling"}
  poi_data = processRawData(xsl_uri, features, bbox)
  output = ''
  recycling_regexp = re.compile(r'recycling:(\w+)')
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if (row['name'] == ''):
      row['name'] = 'Recycling bin(s)'
    recycling_list = []
    has_detail = 0
    for k,v in row.iteritems():
      if (v == 'yes'):
	result = recycling_regexp.search(k)
	if (result):
	  has_detail = 1
	  recycling_list.append(result.groups(0))
    if (has_detail):
      row['description'] = ''.join([row['description'], "<p><strong>Recycling facilities for:</strong> "])
      recycling_list.sort()
      for item in recycling_list:
        row['description'] = ''.join([row['description'], "%s, " % (item)])
      row['description'] = ''.join([row['description'], "</p>"])
    output = ''.join([output, generateKMLPlacemark(row, 'wasteRecyclingBin')])
  return output, myStyles

def feature_amenitytheatre(bbox, myStyles):
  """
    Theatres...
  """
  myStyles["cultureTheatre"] = "culture_theatre.png"
  features = {"amenity":"theatre"}
  output = feature_generic(bbox, "Theatre", "cultureTheatre", features)
  return output, myStyles
    
def feature_amenitywaste_transfer_station(bbox, myStyles):
  """
    Recycling centres...
  """
  myStyles["wasteRecyclingDepot"] = "waste_recycle.png"
  xsl_uri = 'lib/trans_recycling.xsl'
  features = {"amenity":"waste_transfer_station"}
  poi_data = processRawData(xsl_uri, features, bbox)
  output = ''
  recycling_regexp = re.compile(r'recycling:(\w+)')
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if (row['name'] == ''):
      row['name'] = 'Recycling centre'
    recycling_list = []
    has_detail = 0
    for k,v in row.iteritems():
      if (v == 'yes'):
	result = recycling_regexp.search(k)
	if (result):
	  has_detail = 1
	  recycling_list.append(result.groups(0))
    if (has_detail):
      row['description'] = ''.join([row['description'], "<p><strong>Recycling facilities for:</strong> "])
      recycling_list.sort()
      for item in recycling_list:
        row['description'] = ''.join([row['description'], "%s, " % (item)])
      row['description'] = ''.join([row['description'], "</p>"])
    output = ''.join([output, generateKMLPlacemark(row, 'wasteRecyclingDepot')])
  return output, myStyles

def feature_landuseallotments(bbox, myStyles):
  """
    Allotments...
  """
  myStyles["foodAllotment"] = "food_allotment.png"
  myStyles["foodCommunityGrowing"] = "food_community_growing.png"
  xsl_uri = 'lib/trans_generic.xsl'
  features = {"landuse":"allotments"}
  output = ''
  poi_data = processRawData(xsl_uri, features, bbox)
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if (row['community'] == 'yes'):
      iconstyle = "foodCommunityGrowing"
      if (row['name'] == ''):
        row['name'] = 'Community food space'
    else:
      iconstyle = "foodAllotment"
      if (row['name'] == ''):
        row['name'] = 'Allotments'
    output = ''.join([output, generateKMLPlacemark(row, iconstyle)])
  return output, myStyles

def feature_landuselandfill(bbox, myStyles):
  """
    Landfill site...
  """
  myStyles["wasteLandfill"] = "waste_landfill.png"
  features = {"landuse":"landfill"}
  output = feature_generic(bbox, "Landfill site", "wasteLandfill", features)
  return output, myStyles
    
def feature_powergenerator(bbox, myStyles):
  """
    Power generator...
  """
  myStyles["powerSolar"] = "power_solar.png"
  myStyles["powerWind"] = "power_wind.png"
  myStyles["powerBiomass"] = "power_biomass.png"
  myStyles["powerGas"] = "power_gas.png"
  myStyles["powerGeothermal"] = "power_geothermal.png"
  myStyles["powerHydro"] = "power_hydro.png"
  myStyles["powerSea"] = "power_sea.png"
  myStyles["powerWaste"] = "power_waste.png"
  myStyles["powerDefault"] = "power_default.png"
  xsl_uri = 'lib/trans_generators.xsl'
  features = {"power":"generator"}
  poi_data = processRawData(xsl_uri, features, bbox)
  output = ''
  for row in poi_data:
    if (row['lat'] == None):
      continue
    # Skip definitely-un-green sources
    if (row['source'] == 'nuclear' or row['source'] == 'coal'):
      continue
    # Start out with default assumptions
    gen_style = "powerDefault"
    gen_type = "Unknown power generator"
    # Solar panels, geothermal, hydro, tidal, wave or wind turbines? (easy cases)
    if (row['source'] == 'solar'):
      gen_style = "powerSolar"
      if (row['hot_water'] != ''):
        gen_type = "Solar thermal heating panel(s)"
      elif (row['electricity'] != '' and row['method'] == 'thermal'):
	gen_type = "Solar thermal electricity generator"
      elif (row['electricity'] != ''):
        gen_type = "Solar photovoltaic panel(s)"
    elif (row['source'] == 'geothermal'):
      gen_style = 'powerGeothermal'
      if (row['hot_water'] != ''):
        gen_type = "Geothermal heat pump"
      elif (row['electricity'] != ''):
	gen_type = "Geothermal electricity generator"
    elif (row['source'] == 'wind'):
      gen_type = "Wind turbine(s)"
      gen_style = "powerWind"
    elif (row['source'] == 'hydro'):
      gen_type = 'Hydro generator'
      gen_style = 'powerHydro'
    elif (row['source'] == 'tidal'):
      gen_type = 'Tidal generator'
      gen_style = 'powerSea'
    elif (row['source'] == 'wave'):
      gen_type = 'Wave generator'
      gen_style = 'powerSea'
    elif (row['source'] == 'osmotic'):
      gen_type = 'Osmotic generator'
      gen_style = 'powerSea'
    # OK, must be some sort of boiler/CHP/digester/etc.... type of fuel?
    elif (row['source'] == 'biomass'):
      gen_type = "Biomass "
      gen_style = "powerBiomass"
    elif (row['source'] == 'biofuel'):
      gen_type = 'Biofuel '
      gen_style = "powerBiomass"
    elif (row['source'] == 'biogas'):
      gen_type = 'Biogas '
      gen_style = "powerBiomass"
    elif (row['source'] == 'gas'):
      gen_type = 'Gas '
      gen_style = 'powerGas'
    elif (row['source'] == 'oil'):
      gen_type = 'Oil '
      gen_style = "powerDefault"
    elif (row['source'] == 'waste'):
      gen_type = 'Waste-to-energy '
      gen_style = 'powerWaste'
    # Right, means of generation... is it an advanced energy-to-waste plant?
    if (row['method'] == 'anaerobic_digestion'):
      gen_type = ''.join([gen_type, "anaerobic digester"])
    elif (row['method'] == 'pyrolysis'):
      gen_type = ''.join([gen_type, "pyrolising digester"])
    if (row['source'] in ["biomass", "biofuel", "biogas", "gas", "oil", "waste"]):
      # Or maybe just a boiler / stove?
      if (row['electricity'] == '' and (row['hot_water'] != '' or row['hot_air'] != '')):
        if (gen_type == 'Gas '):
	  continue # no interest in gas boilers
        elif (row['hot_water'] != ''):
  	  gen_type = ''.join([gen_type, "boiler"])
        elif (row['hot_air'] != ''):
	  gen_type = ''.join([gen_type, "stove"])
       # Or maybe a CHP/CCHP?
      elif (row['electricity'] != '' and row['cold_water'] == '' and (row['hot_water'] != '' or row['steam'] != '')):
        gen_type = ''.join([gen_type, "combined heat and power plant"])
      elif (row['electricity'] != '' and row['cold_water'] != '' and (row['hot_water'] != '' or row['steam'] != '')):
        gen_type = ''.join([gen_type, "combined heat, cooling and power plant"])
    # For now, skip unknown and fossil generators
    if (gen_type == "Unknown power generator" or gen_type == "Gas " or gen_type == "Oil "):
      continue
    # Description stuff?
    description = "No further details known"
    if (row['description']):
      description = row['description']
    rating = re.compile('\d')
    if (rating.match(row['electricity'])):
      description = ''.join([description, """<p><strong>Electrical rating:</strong> %s</p>""" % (row['electricity'])])
    if (rating.match(row['hot_water'])):
      description = ''.join([description, """<p><strong>Hot water rating:</strong> %s</p>""" % (row['hot_water'])])
    if (rating.match(row['steam'])):
      description = ''.join([description, """<p><strong>Steam rating:</strong> %s</p>""" % (row['steam'])])
    row['description'] = description
    row['name'] = gen_type
    output = ''.join([output, generateKMLPlacemark(row, gen_style)])
  return output, myStyles
    
def feature_railwaystation(bbox, myStyles):
  """
    Train stations...
  """
  myStyles["transportTrain"] = "transport_train.png"
  myStyles["transportDLR"] = "transport_train.png"
  myStyles["transportTube"] = "transport_tube.png"
  xsl_uri = 'lib/trans_generic.xsl'
  features = {"railway":"station"}
  poi_data = processRawData(xsl_uri, features, bbox)
  output = ''
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if (row['tfl_travelzone']):
      row['description'] = ''.join([row['description'], """<p><strong>TfL travel zone:</strong> %s</p>""" % (row['tfl_travelzone'])])
    if (row['network'] == 'London Underground'):
      iconstyle = 'transportTube'
    elif (row['network'] == 'DLR'):
      iconstyle = 'transportDLR'
    else:
      iconstyle = 'transportTrain'
      if (row['ref']):
        row['description'] = ''.join([row['description'], """<p><a href="http://www.nationalrail.co.uk/stations/%s/details.html">Station information</a><br/><a href="http://ojp.nationalrail.co.uk/en/s/ldbboard/dep/%s">Live departure board</a>.</p>""" % (row['ref'], row['ref'])])
    output = ''.join([output, generateKMLPlacemark(row, iconstyle)])
  return output, myStyles
    
def feature_railwaytram_stop(bbox, myStyles):
  """
    Tram stops...
  """
  myStyles["transportTram"] = "transport_tram.png"
  features = {"railway":"tram_stop"}
  output = feature_generic(bbox, "Tram stop", "transportTram", features)
  return output, myStyles

def feature_tourismgallery(bbox, myStyles):
  """
    Art galleries...
  """
  myStyles["cultureGallery"] = "culture_gallery.png"
  features = {"tourism":"gallery"}
  output = feature_generic(bbox, "Art gallery", "cultureGallery", features)
  return output, myStyles

def feature_tourismmuseum(bbox, myStyles):
  """
    Museums...
  """
  myStyles["cultureMuseum"] = "culture_museum.png"
  features = {"tourism":"museum"}
  output = feature_generic(bbox, "Museum", "cultureMuseum", features)
  return output, myStyles
