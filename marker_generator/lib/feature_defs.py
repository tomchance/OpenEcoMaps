# -*- coding: utf-8 -*-
#! /usr/bin/python

"""
  feature_defs.py
  Copyright 2010-13 Tom Chance <tom@acrewoods.net>

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

__author__ = "Tom Chance"
__email__ = "tom@acrewoods.net"
__copyright__ = "Copyright 2010-13, Tom Chance"
__license__ = "GPL"

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

def feature_bicycle_parking(bbox, myStyles):
  """
    Bicycle parking stands...
  """
  myStyles["transportCycleParking"] = "transport_cycle_parking.png"
  features = "amenity=bicycle_parking"
  output = feature_generic(bbox, "Cycle parking stand", "transportCycleParking", features)
  return output, myStyles
    
def feature_bicycle_rental(bbox, myStyles):
  """
    Bike hire...
  """
  myStyles["transportCyclehire"] = "transport_cyclehire.png"
  xsl_uri = 'lib/trans_generic.xsl'
  features = "amenity=bicycle_rental"
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

def feature_car_sharing(bbox, myStyles):
  """
    Car club parking bays...
  """
  myStyles["transportCarshare"] = "transport_carsharing.png"
  features = "amenity=car_sharing"
  output = feature_generic(bbox, "Car club parking bay", "transportCarshare", features)
  return output, myStyles

def feature_cinema(bbox, myStyles):
  """
    Cinemas...
  """
  myStyles["cultureCinema"] = "culture_cinema.png"
  features = "amenity=cinema"
  output = feature_generic(bbox, "Cinema", "cultureCinema", features)
  return output, myStyles

def feature_library(bbox, myStyles):
  """
    Libraries...
  """
  myStyles["cultureLibrary"] = "culture_library.png"
  features = "amenity=library"
  output = feature_generic(bbox, "Library", "cultureLibrary", features)
  return output, myStyles
    
def feature_marketplace(bbox, myStyles):
  """
    Food markets...
  """
  myStyles["foodMarket"] = "food_market.png"
  xsl_uri = 'lib/trans_food.xsl'
  features = "amenity=marketplace"
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
    
def feature_recycling(bbox, myStyles):
  """
    Recycling bins...
  """
  myStyles["wasteRecyclingBin"] = "waste_recycle.png"
  xsl_uri = 'lib/trans_recycling.xsl'
  features = "amenity=recycling"
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

def feature_theatre(bbox, myStyles):
  """
    Theatres...
  """
  myStyles["cultureTheatre"] = "culture_theatre.png"
  features = "amenity=theatre"
  output = feature_generic(bbox, "Theatre", "cultureTheatre", features)
  return output, myStyles
    
def feature_waste_transfer_station(bbox, myStyles):
  """
    Recycling centres...
  """
  myStyles["wasteRecyclingDepot"] = "waste_recycle.png"
  xsl_uri = 'lib/trans_recycling.xsl'
  features = "amenity=waste_transfer_station"
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

def feature_vegetarian(bbox, myStyles):
  """
    Vegetarian, vegan and meat-free restaurants, cafes, etc...
  """
  myStyles["veggieBakery"] = "food_bakery_grey.png"
  myStyles["veggieFarmShop"] = "food_farmers_grey.png"
  myStyles["veggieGreengrocer"] = "food_greengrocer_grey.png"
  myStyles["veggieConvenience"] = "food_convenience_grey.png"
  myStyles["veggieCafe"] = "food_cafe_grey.png"
  myStyles["veggieRestaurant"] = "food_restaurant_grey.png"
  myStyles["veggieTakeaway"] = "food_takeaway_grey.png"
  myStyles["veggieBakeryOnly"] = "food_bakery.png"
  myStyles["veggieFarmShopOnly"] = "food_farmers.png"
  myStyles["veggieGreengrocerOnly"] = "food_greengrocer.png"
  myStyles["veggieConvenienceOnly"] = "food_convenience.png"
  myStyles["veggieCafeOnly"] = "food_cafe.png"
  myStyles["veggieRestaurantOnly"] = "food_restaurant.png"
  myStyles["veggieTakeawayOnly"] = "food_takeaway.png"
  xsl_uri = 'lib/trans_food.xsl'
  output = ''
  features = "diet:vegetarian|diet:vegan=yes|only"
  #features="cuisine=vegetarian|vegan"
  poi_data = processRawData(xsl_uri, features, bbox)
  yn = ["yes", "no", "only"]
  for row in poi_data:
    if (row['name'] == None):
      continue
    if (row['amenity'] == "cafe"):
      iconstyle = "veggieCafe"
      row['name'] = ''.join([row['name'], " (cafe)"])
    elif (row['amenity'] == "restaurant" or row['amenity'] == "pub"):
      iconstyle = "veggieRestaurant"
      row['name'] = ''.join([row['name'], " (restaurant/pub)"])
    elif (row['amenity'] == "fast_food"):
      iconstyle = "veggieTakeaway"
      row['name'] = ''.join([row['name'], " (takeaway)"])
    elif (row['shop'] == "baker"):
      iconstyle = "veggieBakery"
      row['name'] = ''.join([row['name'], " (bakery)"])
    elif (row['shop'] == "farm"):
      iconstyle = "veggieFarmShop"
      row['name'] = ''.join([row['name'], " (farm shop)"])
    elif (row['shop'] == "greengrocer"):
      iconstyle = "veggieGreengrocer"
      row['name'] = ''.join([row['name'], " (greengrocer)"])
    elif (row['shop'] == "convenience"):
      iconstyle = "veggieConvenience"
      row['name'] = ''.join([row['name'], " (corner shop)"])
    elif (row['shop'] == "supermarket"):
      iconstyle = "veggieConvenience"
      row['name'] = ''.join([row['name'], " (supermarket)"])
    else:
      continue
    if (row['diet:vegetarian'] == 'only' or row['diet:vegan'] == 'only'):
      iconstyle = ''.join([iconstyle, 'Only'])
    if (row['cuisine']):
      row['description'] = ''.join(["<p><strong>Cuisine:</strong> %s</p>" % (row['cuisine']), row['description']])
    if (row['diet:vegetarian'] in yn):
      row['description'] = ''.join(["<p><strong>Vegetarian:</strong> %s</p>" % (row['diet:vegetarian']), row['description']])
    if (row['diet:vegan'] in yn):
      row['description'] = ''.join(["<p><strong>Vegan:</strong> %s</p>" % (row['diet:vegan']), row['description']])
    output = ''.join([output, generateKMLPlacemark(row, iconstyle)])
  return output, myStyles

def feature_fruittree(bbox, myStyles):
  """
    Trees with fruit or nuts
  """
  myStyles["foodFruitTree"] = "food_fruit_tree.png"
  xsl_uri = 'lib/trans_trees.xsl'
  output = ''
  features="produce=*"
  poi_data = processRawData(xsl_uri, features, bbox)
  iconstyle = 'foodFruitTree'
  for row in poi_data:
    if (row['name'] == None):
      continue
    if (row['produce']):
      row['description'] = ''.join(["<p><strong>Fruit/nuts:</strong> %s</p>" % (row['produce']), row['description']])
    if (row['species:en']):
      row['description'] = ''.join(["<p><strong>Tree common name:</strong> %s</p>" % (row['species:en']), row['description']])
    if (row['species']):
      row['description'] = ''.join(["<p><strong>Tree species:</strong> %s</p>" % (row['species']), row['description']])
    output = ''.join([output, generateKMLPlacemark(row, iconstyle)])
  return output, myStyles

def feature_bus_stop(bbox, myStyles):
  """
    Bus stops...
  """
  myStyles["transportBusStop"] = "transport_bus.png"
  features = "highway=bus_stop"
  output = feature_generic(bbox, "Bus stop", "transportBusStop", features)
  return output, myStyles

def feature_allotments(bbox, myStyles):
  """
    Allotments...
  """
  myStyles["foodAllotment"] = "food_allotment.png"
  myStyles["foodCommunityGrowing"] = "food_community_growing.png"
  xsl_uri = 'lib/trans_generic.xsl'
  features = "landuse=allotments"
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

def feature_landfill(bbox, myStyles):
  """
    Landfill site...
  """
  myStyles["wasteLandfill"] = "waste_landfill.png"
  features = "landuse=landfill"
  output = feature_generic(bbox, "Landfill site", "wasteLandfill", features)
  return output, myStyles
    
def feature_powergenerator(bbox, myStyles, server):
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
  poi_data = processRawData('power','generator', bbox, server)
  output = []
  for row in poi_data:
    if (row['lat'] == None):
      continue
    # Skip generators without a source with which to categorise
    if ('generator:source' not in row):
      continue
    # Skip definitely-un-green sources
    if (row['generator:source'] == 'nuclear' or row['generator:source'] == 'coal'):
      continue
    # Start out with default assumptions
    gen_style = "powerDefault"
    gen_type = "Unknown power generator"
    # Solar panels, geothermal, hydro, tidal, wave or wind turbines? (easy cases)
    if (row['generator:source'] == 'solar'):
      gen_style = "powerSolar"
      if ('generator:output:hot_water' in row):
        gen_type = "Solar thermal heating panel(s)"
      elif ('generator:output:electricity' in row and row['generator:method'] == 'thermal'):
        gen_type = "Solar thermal electricity generator"
      elif ('generator:output:electricity' in row):
        gen_type = "Solar photovoltaic panel(s)"
    elif (row['generator:source'] == 'geothermal'):
      gen_style = 'powerGeothermal'
      if ('generator:output:hot_water' in row):
        gen_type = "Geothermal heat pump"
      elif ('generator:output:electricity' in row):
        gen_type = "Geothermal electricity generator"
    elif (row['generator:source'] == 'wind'):
      gen_type = "Wind turbine(s)"
      gen_style = "powerWind"
    elif (row['generator:source'] == 'hydro'):
      gen_type = 'Hydro generator'
      gen_style = 'powerHydro'
    elif (row['generator:source'] == 'tidal'):
      gen_type = 'Tidal generator'
      gen_style = 'powerSea'
    elif (row['generator:source'] == 'wave'):
      gen_type = 'Wave generator'
      gen_style = 'powerSea'
    elif (row['generator:source'] == 'osmotic'):
      gen_type = 'Osmotic generator'
      gen_style = 'powerSea'
    # OK, must be some sort of boiler/CHP/digester/etc.... type of fuel?
    elif (row['generator:source'] == 'biomass'):
      gen_type = "Biomass "
      gen_style = "powerBiomass"
    elif (row['generator:source'] == 'biofuel'):
      gen_type = 'Biofuel '
      gen_style = "powerBiomass"
    elif (row['generator:source'] == 'biogas'):
      gen_type = 'Biogas '
      gen_style = "powerBiomass"
    elif (row['generator:source'] == 'gas'):
      gen_type = 'Gas '
      gen_style = 'powerGas'
    elif (row['generator:source'] == 'oil'):
      gen_type = 'Oil '
      gen_style = "powerDefault"
    elif (row['generator:source'] == 'waste'):
      gen_type = 'Waste-to-energy '
      gen_style = 'powerWaste'
    # Right, means of generation... is it an advanced energy-to-waste plant?
    if ('generator:method' in row and row['generator:method'] == 'anaerobic_digestion'):
      gen_type = ''.join([gen_type, "anaerobic digester"])
    elif ('generator:method' in row and row['generator:method'] == 'pyrolysis'):
      gen_type = ''.join([gen_type, "pyrolising digester"])
    if (row['generator:source'] in ["biomass", "biofuel", "biogas", "gas", "oil", "waste"]):
      # Or maybe just a boiler / stove?
      if ('generator:output:electricity' not in row and ('generator:output:hot_water' in row or 'generator:output:hot_air' in row)):
        if (gen_type == 'Gas '):
          continue # no interest in gas boilers
        elif ('generator:output:hot_water' in row):
          gen_type = ''.join([gen_type, "boiler"])
        elif ('generator:output:hot_air'  in row):
          gen_type = ''.join([gen_type, "stove"])
      # Or maybe a CHP/CCHP?
      elif ('generator:output:electricity' in row and 'generator:output:cold_water' not in row and ('generator:output:hot_water' in row or 'generator:output:steam' in row)):
        gen_type = ''.join([gen_type, "combined heat and power plant"])
      elif ('generator:output:electricity' in row and 'generator:output:cold_water' in row and ('generator:output:hot_water' in row or 'generator:output:steam' in row)):
        gen_type = ''.join([gen_type, "combined heat, cooling and power plant"])
    # For now, skip unknown and fossil generators
    if (gen_type == "Unknown power generator" or gen_type == "Gas " or gen_type == "Oil "):
      continue
    # Description stuff?
    description = "No further details known"
    if ('description' in row):
      description = row['description']
    rating = re.compile('\d')
    if ('generator:output:electricity' in row and rating.match(row['generator:output:electricity'])):
      description = ''.join([description, """<p><strong>Electrical rating:</strong> %s</p>""" % (row['generator:output:electricity'])])
    if ('generator:output:hot_water' in row and rating.match(row['generator:output:hot_water'])):
      description = ''.join([description, """<p><strong>Hot water rating:</strong> %s</p>""" % (row['generator:output:hot_water'])])
    if ('generator:output:steam' in row and rating.match(row['generator:output:steam'])):
      description = ''.join([description, """<p><strong>Steam rating:</strong> %s</p>""" % (row['generator:output:steam'])])
    row['popup_title'] = gen_type
    row['popup_contents'] = description
    row['popup_style'] = gen_style
    output.append(row)
  return output, myStyles
    
def feature_railwaystation(bbox, myStyles):
  """
    Train stations...
  """
  myStyles["transportTrain"] = "transport_train.png"
  myStyles["transportDLR"] = "transport_train.png"
  myStyles["transportTube"] = "transport_tube.png"
  xsl_uri = 'lib/trans_generic.xsl'
  features = "railway=station"
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
    
def feature_tram_stop(bbox, myStyles):
  """
    Tram stops...
  """
  myStyles["transportTram"] = "transport_tram.png"
  features = "railway=tram_stop"
  output = feature_generic(bbox, "Tram stop", "transportTram", features)
  return output, myStyles

def feature_bakery(bbox, myStyles):
  """
    Bakeries...
  """
  myStyles["foodBakery"] = "food_bakery.png"
  features = "shop=bakery"
  output = feature_generic(bbox, "Bakery", "foodBakery", features)
  return output, myStyles

def feature_butcher(bbox, myStyles):
  """
    Butchers...
  """
  myStyles["foodButcher"] = "food_butcher.png"
  features = "shop=butcher"
  output = feature_generic(bbox, "Butcher", "foodButcher", features)
  return output, myStyles

def feature_farmshop(bbox, myStyles):
  """
    Farmers shop...
  """
  myStyles["foodFarmShop"] = "food_farmers.png"
  features = "shop=farm"
  output = feature_generic(bbox, "Farm shop", "foodFarmShop", features)
  return output, myStyles

def feature_seafood(bbox, myStyles):
  """
    Fishmongers...
  """
  myStyles["foodFishmonger"] = "food_fishmonger.png"
  features = "shop=seafood"
  output = feature_generic(bbox, "Fishmonger", "foodFishmonger", features)
  return output, myStyles

def feature_greengrocer(bbox, myStyles):
  """
    Greengrocers...
  """
  myStyles["foodGreengrocer"] = "food_greengrocer.png"
  features = "shop=greengrocer"
  output = feature_generic(bbox, "Greengrocer", "foodGreengrocer", features)
  return output, myStyles

def feature_gallery(bbox, myStyles):
  """
    Art galleries...
  """
  myStyles["cultureGallery"] = "culture_gallery.png"
  features = "tourism=gallery"
  output = feature_generic(bbox, "Art gallery", "cultureGallery", features)
  return output, myStyles

def feature_museum(bbox, myStyles):
  """
    Museums...
  """
  myStyles["cultureMuseum"] = "culture_museum.png"
  features = "tourism=museum"
  output = feature_generic(bbox, "Museum", "cultureMuseum", features)
  return output, myStyles
