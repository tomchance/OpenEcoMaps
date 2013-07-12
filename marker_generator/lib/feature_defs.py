# -*- coding: utf-8 -*-
#! /usr/bin/python

'''
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
'''

__author__ = 'Tom Chance'
__email__ = 'tom@acrewoods.net'
__copyright__ = 'Copyright 2010-13, Tom Chance'
__license__ = 'GPL'

from lib.osm_processing import *
from lib.kml_processing import *
import re

def feature_generic(bbox, defaultName, style, key, value, server):
  '''
    Generic features (no fancy data processing required for
    the description)
  '''
  output = []
  poi_data = processRawData(key, value, bbox, server)
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if ('name' in row):
      row['popup_title'] = row['name']
    else:
      row['popup_title'] = defaultName
    if ('description' in row):
      row['popup_contents'] = row['description']
    else:
      row['popup_contents'] = ''
    row['popup_style'] = style
    output.append(row)
  return output

def feature_bicycle_parking(bbox, myStyles, server):
  '''
    Bicycle parking stands...
  '''
  myStyles['transportCycleParking'] = 'transport_cycle_parking.png'
  output = feature_generic(bbox, 'Cycle parking stand', 'transportCycleParking', 'amenity', 'bicycle_parking', server)
  return output, myStyles
    
def feature_bicycle_rental(bbox, myStyles, server):
  '''
    Bike hire...
  '''
  myStyles['transportCyclehire'] = 'transport_cyclehire.png'
  poi_data = processRawData('amenity', 'bicycle_rental', bbox, server)
  output = []
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if ('name' in row):
      row['popup_title'] = row['name']
    else:
      row['popup_title'] = 'Cycle hire docking bay'
    if ('network' in row):
      if (row['network'] == 'Barclays Cycle Hire'):
        row['popup_title'] = ''.join(['TfL Cycle Hire: ', row['popup_title']])
    if ('description' in row):
      row['popup_contents'] = row['description']
    else:
      row['popup_contents'] = ''
    if ('capacity' in row):
      row['popup_contents'] = ''.join([row['popup_contents'], '<p><strong>Capacity:</strong> %s</p>' % (row['capacity'])])
    row['popup_style'] = 'transportCyclehire'
    output.append(row)
  return output, myStyles

def feature_car_sharing(bbox, myStyles, server):
  '''
    Car club parking bays...
  '''
  myStyles['transportCarshare'] = 'transport_carsharing.png'
  output = feature_generic(bbox, 'Car club parking bay', 'transportCarshare', 'amenity', 'car_sharing', server)
  return output, myStyles

def feature_cinema(bbox, myStyles, server):
  '''
    Cinemas...
  '''
  myStyles['cultureCinema'] = 'culture_cinema.png'
  output = feature_generic(bbox, 'Cinema', 'cultureCinema', 'amenity', 'cinema', server)
  return output, myStyles

def feature_library(bbox, myStyles, server):
  '''
    Libraries...
  '''
  myStyles['cultureLibrary'] = 'culture_library.png'
  output = feature_generic(bbox, 'Library', 'cultureLibrary', 'amenity', 'library', server)
  return output, myStyles
    
def feature_marketplace(bbox, myStyles, server):
  '''
    Food markets...
  '''
  myStyles['foodMarket'] = 'food_market.png'
  poi_data = processRawData('amenity', 'marketplace', bbox, server)
  output = []
  for row in poi_data:
    if (row['lat'] == None):
      continue
    # Skip markets that don't sell fish/meat/veg
    if (row.get('vegetables') != 'yes' and row.get('meat') != 'yes' and row.get('fish') != 'yes'):
      continue
    if ('name' in row):
      row['popup_title'] = row['name']
    else:
      row['popup_title'] = 'Food market'
    row['popup_style'] = 'foodMarket'
    if ('description' in row):
      row['popup_contents'] = row['description']
    else:
      row['popup_contents'] = ''
    output.append(row)
  return output, myStyles
    
def feature_recycling(bbox, myStyles, server):
  '''
    Recycling bins...
  '''
  myStyles['wasteRecyclingBin'] = 'waste_recycle.png'
  poi_data = processRawData('amenity', 'recycling', bbox, server)
  output = []
  recycling_regexp = re.compile(r'recycling:(\w+)')
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if ('name' in row):
      row['popup_title'] = row['name']
    else:
      row['popup_title'] = 'Recycling bin(s)'
    if ('description' in row):
      row['popup_contents'] = row['description']
    else:
      row['popup_contents'] = ''
    recycling_list = []
    has_detail = 0
    for k,v in row.iteritems():
      if (v == 'yes'):
        result = recycling_regexp.search(k)
        if (result):
          has_detail = 1
          recycling_list.append(result.groups(0))
    if (has_detail):
      row['popup_contents'] = ''.join([row['popup_contents'], '<p><strong>Recycling facilities for:</strong> '])
      recycling_list.sort()
      for item in recycling_list:
        row['popup_contents'] = ''.join([row['popup_contents'], '%s, ' % (item)])
      row['popup_contents'] = ''.join([row['popup_contents'], '</p>'])
    row['popup_style'] = 'wasteRecyclingBin'
    output.append(row)
  return output, myStyles

def feature_theatre(bbox, myStyles, server):
  '''
    Theatres...
  '''
  myStyles['cultureTheatre'] = 'culture_theatre.png'
  output = feature_generic(bbox, 'Theatre', 'cultureTheatre', 'amenity', 'theatre', server)
  return output, myStyles
    
def feature_waste_transfer_station(bbox, myStyles, server):
  '''
    Recycling centres...
  '''
  myStyles['wasteRecyclingDepot'] = 'waste_recycle.png'
  poi_data = processRawData('amenity', 'waste_transfer_station', bbox, server)
  output = []
  recycling_regexp = re.compile(r'recycling:(\w+)')
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if ('name' in row):
      row['popup_title'] = row['name']
    else:
      row['popup_title'] = 'Recycling centre'
    if ('description' in row):
      row['popup_contents'] = row['description']
    else:
      row['popup_contents'] = ''
    recycling_list = []
    has_detail = 0
    for k,v in row.iteritems():
      if (v == 'yes'):
        result = recycling_regexp.search(k)
        if (result):
          has_detail = 1
          recycling_list.append(result.groups(0))
    if (has_detail):
      row['popup_contents'] = ''.join([row['popup_contents'], '<p><strong>Recycling facilities for:</strong> '])
      recycling_list.sort()
      for item in recycling_list:
        row['popup_contents'] = ''.join([row['popup_contents'], '%s, ' % (item)])
      row['popup_contents'] = ''.join([row['popup_contents'], '</p>'])
    row['popup_style'] = 'wasteRecyclingDepot'
    output.append(row)
  return output, myStyles

def feature_vegetarian(bbox, myStyles, server):
  '''
    Vegetarian, vegan and meat-free restaurants, cafes, etc...
  '''
  myStyles['veggieBakery'] = 'food_bakery_grey.png'
  myStyles['veggieFarmShop'] = 'food_farmers_grey.png'
  myStyles['veggieGreengrocer'] = 'food_greengrocer_grey.png'
  myStyles['veggieConvenience'] = 'food_convenience_grey.png'
  myStyles['veggieCafe'] = 'food_cafe_grey.png'
  myStyles['veggieRestaurant'] = 'food_restaurant_grey.png'
  myStyles['veggieTakeaway'] = 'food_takeaway_grey.png'
  myStyles['veggieBakeryOnly'] = 'food_bakery.png'
  myStyles['veggieFarmShopOnly'] = 'food_farmers.png'
  myStyles['veggieGreengrocerOnly'] = 'food_greengrocer.png'
  myStyles['veggieConvenienceOnly'] = 'food_convenience.png'
  myStyles['veggieCafeOnly'] = 'food_cafe.png'
  myStyles['veggieRestaurantOnly'] = 'food_restaurant.png'
  myStyles['veggieTakeawayOnly'] = 'food_takeaway.png'
  output = []
  poi_data = processRawData('diet:vegetarian', 'yes|only', bbox, server) + processRawData('diet:vegan', 'yes|only', bbox, server)
  yn = ['yes', 'no', 'only']
  for row in poi_data:
    if ('name' not in row):
      continue
    if (row.get('amenity') == 'cafe'):
      row['popup_style'] = 'veggieCafe'
      row['popup_title'] = ''.join([row.get('name'), ' (cafe)'])
    elif (row.get('amenity') == 'restaurant' or row.get('amenity') == 'pub'):
      row['popup_style'] = 'veggieRestaurant'
      row['popup_title'] = ''.join([row.get('name'), ' (restaurant/pub)'])
    elif (row.get('amenity') == 'fast_food'):
      row['popup_style'] = 'veggieTakeaway'
      row['popup_title'] = ''.join([row.get('name'), ' (takeaway)'])
    elif (row.get('shop') == 'baker'):
      row['popup_style'] = 'veggieBakery'
      row['popup_title'] = ''.join([row.get('name'), ' (bakery)'])
    elif (row.get('shop') == 'farm'):
      row['popup_style'] = 'veggieFarmShop'
      row['popup_title'] = ''.join([row.get('name'), ' (farm shop)'])
    elif (row.get('shop') == 'greengrocer'):
      row['popup_style'] = 'veggieGreengrocer'
      row['popup_title'] = ''.join([row.get('name'), ' (greengrocer)'])
    elif (row.get('shop') == 'convenience'):
      row['popup_style'] = 'veggieConvenience'
      row['popup_title'] = ''.join([row.get('name'), ' (corner shop)'])
    elif (row.get('shop') == 'supermarket'):
      row['popup_style'] = 'veggieConvenience'
      row['popup_title'] = ''.join([row.get('name'), ' (supermarket)'])
    else:
      continue
    if (row.get('diet:vegetarian') == 'only' or row.get('diet:vegan') == 'only'):
      row['popup_style'] = ''.join([row['popup_style'], 'Only'])
    if ('description' in row):
      row['popup_contents'] = row['description']
    else:
      row['popup_contents'] = ''
    if (row.get('cuisine')):
      row['popup_contents'] = ''.join(['<p><strong>Cuisine:</strong> %s</p>' % (row.get('cuisine')), row['popup_contents']])
    if (row.get('diet:vegetarian') in yn):
      row['popup_contents'] = ''.join(['<p><strong>Vegetarian:</strong> %s</p>' % (row.get('diet:vegetarian')), row['popup_contents']])
    if (row.get('diet:vegan') in yn):
      row['popup_contents'] = ''.join(['<p><strong>Vegan:</strong> %s</p>' % (row.get('diet:vegan')), row['popup_contents']])
    output.append(row)
  return output, myStyles

def feature_fruittree(bbox, myStyles, server):
  '''
    Trees with fruit or nuts
  '''
  myStyles['foodFruitTree'] = 'food_fruit_tree.png'
  output = []
  poi_data = processRawData('produce', '', bbox, server)
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if ('name' in row):
      row['popup_title'] = row['name']
    else:
      row['popup_title'] = 'Fruit tree'
    if ('description' in row):
      row['popup_contents'] = row['description']
    else:
      row['popup_contents'] = ''
    row['popup_style'] = 'foodFruitTree'
    if (row.get('produce')):
      row['popup_contents'] = ''.join(['<p><strong>Fruit/nuts:</strong> %s</p>' % (row['produce']), row['popup_contents']])
    if (row.get('species:en')):
      row['popup_contents'] = ''.join(['<p><strong>Tree common name:</strong> %s</p>' % (row['species:en']), row['popup_contents']])
    if (row.get('species')):
      row['popup_contents'] = ''.join(['<p><strong>Tree species:</strong> %s</p>' % (row['species']), row['popup_contents']])
    output.append(row)
  return output, myStyles

def feature_bus_stop(bbox, myStyles, server):
  '''
    Bus stops...
  '''
  myStyles['transportBusStop'] = 'transport_bus.png'
  output = feature_generic(bbox, 'Bus stop', 'transportBusStop', 'highway', 'bus_stop', server)
  return output, myStyles

def feature_allotments(bbox, myStyles, server):
  '''
    Allotments...
  '''
  myStyles['foodAllotment'] = 'food_allotment.png'
  myStyles['foodCommunityGrowing'] = 'food_community_growing.png'
  output = []
  poi_data = processRawData('landuse', 'allotments', bbox, server)
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if ('name' in row):
      row['popup_title'] = row['name']
    if ('community' in row and row['community'] == 'yes'):
      row['popup_style'] = 'foodCommunityGrowing'
      if ('name' not in row):
        row['popup_title'] = 'Community food space'
    else:
      row['popup_style'] = 'foodAllotment'
      if ('name' not in row):
        row['popup_title'] = 'Allotments'
    if ('description' in row):
      row['popup_contents'] = row['description']
    else:
      row['popup_contents'] = ''
    output.append(row)
  return output, myStyles

def feature_landfill(bbox, myStyles, server):
  '''
    Landfill site...
  '''
  myStyles['wasteLandfill'] = 'waste_landfill.png'
  output = feature_generic(bbox, 'Landfill site', 'wasteLandfill', 'landuse', 'landfill', server)
  return output, myStyles
    
def feature_powergenerator(bbox, myStyles, server):
  '''
    Power generator...
  '''
  myStyles['powerSolar'] = 'power_solar.png'
  myStyles['powerWind'] = 'power_wind.png'
  myStyles['powerBiomass'] = 'power_biomass.png'
  myStyles['powerGas'] = 'power_gas.png'
  myStyles['powerGeothermal'] = 'power_geothermal.png'
  myStyles['powerHydro'] = 'power_hydro.png'
  myStyles['powerSea'] = 'power_sea.png'
  myStyles['powerWaste'] = 'power_waste.png'
  myStyles['powerDefault'] = 'power_default.png'
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
    gen_style = 'powerDefault'
    gen_type = 'Unknown power generator'
    # Solar panels, geothermal, hydro, tidal, wave or wind turbines? (easy cases)
    if (row['generator:source'] == 'solar'):
      gen_style = 'powerSolar'
      if ('generator:output:hot_water' in row):
        gen_type = 'Solar thermal heating panel(s)'
      elif ('generator:output:electricity' in row and row['generator:method'] == 'thermal'):
        gen_type = 'Solar thermal electricity generator'
      elif ('generator:output:electricity' in row):
        gen_type = 'Solar photovoltaic panel(s)'
    elif (row['generator:source'] == 'geothermal'):
      gen_style = 'powerGeothermal'
      if ('generator:output:hot_water' in row):
        gen_type = 'Geothermal heat pump'
      elif ('generator:output:electricity' in row):
        gen_type = 'Geothermal electricity generator'
    elif (row['generator:source'] == 'wind'):
      gen_type = 'Wind turbine(s)'
      gen_style = 'powerWind'
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
      gen_type = 'Biomass '
      gen_style = 'powerBiomass'
    elif (row['generator:source'] == 'biofuel'):
      gen_type = 'Biofuel '
      gen_style = 'powerBiomass'
    elif (row['generator:source'] == 'biogas'):
      gen_type = 'Biogas '
      gen_style = 'powerBiomass'
    elif (row['generator:source'] == 'gas'):
      gen_type = 'Gas '
      gen_style = 'powerGas'
    elif (row['generator:source'] == 'oil'):
      gen_type = 'Oil '
      gen_style = 'powerDefault'
    elif (row['generator:source'] == 'waste'):
      gen_type = 'Waste-to-energy '
      gen_style = 'powerWaste'
    # Right, means of generation... is it an advanced energy-to-waste plant?
    if ('generator:method' in row and row['generator:method'] == 'anaerobic_digestion'):
      gen_type = ''.join([gen_type, 'anaerobic digester'])
    elif ('generator:method' in row and row['generator:method'] == 'pyrolysis'):
      gen_type = ''.join([gen_type, 'pyrolising digester'])
    if (row['generator:source'] in ['biomass', 'biofuel', 'biogas', 'gas', 'oil', 'waste']):
      # Or maybe just a boiler / stove?
      if ('generator:output:electricity' not in row and ('generator:output:hot_water' in row or 'generator:output:hot_air' in row)):
        if (gen_type == 'Gas '):
          continue # no interest in gas boilers
        elif ('generator:output:hot_water' in row):
          gen_type = ''.join([gen_type, 'boiler'])
        elif ('generator:output:hot_air'  in row):
          gen_type = ''.join([gen_type, 'stove'])
      # Or maybe a CHP/CCHP?
      elif ('generator:output:electricity' in row and 'generator:output:cold_water' not in row and ('generator:output:hot_water' in row or 'generator:output:steam' in row)):
        gen_type = ''.join([gen_type, 'combined heat and power plant'])
      elif ('generator:output:electricity' in row and 'generator:output:cold_water' in row and ('generator:output:hot_water' in row or 'generator:output:steam' in row)):
        gen_type = ''.join([gen_type, 'combined heat, cooling and power plant'])
    # For now, skip unknown and fossil generators
    if (gen_type == 'Unknown power generator' or gen_type == 'Gas ' or gen_type == 'Oil '):
      continue
    # Description stuff?
    description = 'No further details known.'
    if ('description' in row):
      description = row['description']
    rating = re.compile('\d')
    if ('generator:output:electricity' in row and rating.match(row['generator:output:electricity'])):
      description = ''.join([description, '''<p><strong>Electrical rating:</strong> %s</p>''' % (row['generator:output:electricity'])])
    if ('generator:output:hot_water' in row and rating.match(row['generator:output:hot_water'])):
      description = ''.join([description, '''<p><strong>Hot water rating:</strong> %s</p>''' % (row['generator:output:hot_water'])])
    if ('generator:output:steam' in row and rating.match(row['generator:output:steam'])):
      description = ''.join([description, '''<p><strong>Steam rating:</strong> %s</p>''' % (row['generator:output:steam'])])
    row['popup_title'] = gen_type
    row['popup_contents'] = description
    row['popup_style'] = gen_style
    output.append(row)
  return output, myStyles

def feature_railwaystation(bbox, myStyles, server):
  '''
    Train stations...
  '''
  myStyles['transportTrain'] = 'transport_train.png'
  myStyles['transportDLR'] = 'transport_train.png'
  myStyles['transportTube'] = 'transport_tube.png'
  poi_data = processRawData('railway', 'station', bbox, server)
  output = []
  for row in poi_data:
    if (row['lat'] == None):
      continue
    if ('name' in row):
      row['popup_title'] = row['name']
    else:
      row['popup_title'] = 'Railway station'
    if ('description' in row):
      row['popup_contents'] = row['name']
    else:
      row['popup_contents'] = ''
    if ('tfl_travelzone' in row):
      row['popup_contents'] = ''.join([row['popup_contents'], '''<p><strong>TfL travel zone:</strong> %s</p>''' % (row['tfl_travelzone'])])
    if ('ref' in row):
      row['popup_contents'] = ''.join([row['popup_contents'], '''<p><a href="http://www.nationalrail.co.uk/stations/%s/details.html">Station information</a><br/><a href="http://ojp.nationalrail.co.uk/en/s/ldbboard/dep/%s">Live departure board</a>.</p>''' % (row['ref'], row['ref'])])
    row['popup_style'] = 'transportTrain'
    if ('network' in row):
      if (row['network'] == 'London Underground'):
        row['popup_style'] = 'transportTube'
      elif (row['network'] == 'DLR'):
        row['popup_style'] = 'transportDLR'
    output.append(row)
  return output, myStyles
    
def feature_tram_stop(bbox, myStyles, server):
  '''
    Tram stops...
  '''
  myStyles['transportTram'] = 'transport_tram.png'
  output = feature_generic(bbox, 'Tram stop', 'transportTram', 'railway', 'tram_stop', server)
  return output, myStyles

def feature_bakery(bbox, myStyles, server):
  '''
    Bakeries...
  '''
  myStyles['foodBakery'] = 'food_bakery.png'
  output = feature_generic(bbox, 'Bakery', 'foodBakery', 'shop', 'bakery', server)
  return output, myStyles

def feature_butcher(bbox, myStyles, server):
  '''
    Butchers...
  '''
  myStyles['foodButcher'] = 'food_butcher.png'
  output = feature_generic(bbox, 'Butcher', 'foodButcher', 'shop', 'butcher', server)
  return output, myStyles

def feature_farmshop(bbox, myStyles, server):
  '''
    Farmers shop...
  '''
  myStyles['foodFarmShop'] = 'food_farmers.png'
  output = feature_generic(bbox, 'Farm shop', 'foodFarmShop', 'shop', 'farm', server)
  return output, myStyles

def feature_seafood(bbox, myStyles, server):
  '''
    Fishmongers...
  '''
  myStyles['foodFishmonger'] = 'food_fishmonger.png'
  output = feature_generic(bbox, 'Fishmonger', 'foodFishmonger', 'shop', 'seafood', server)
  return output, myStyles

def feature_greengrocer(bbox, myStyles, server):
  '''
    Greengrocers...
  '''
  myStyles['foodGreengrocer'] = 'food_greengrocer.png'
  output = feature_generic(bbox, 'Greengrocer', 'foodGreengrocer', 'shop', 'greengrocer', server)
  return output, myStyles

def feature_gallery(bbox, myStyles, server):
  '''
    Art galleries...
  '''
  myStyles['cultureGallery'] = 'culture_gallery.png'
  output = feature_generic(bbox, 'Art gallery', 'cultureGallery', 'tourism', 'gallery', server)
  return output, myStyles

def feature_museum(bbox, myStyles, server):
  '''
    Museums...
  '''
  myStyles['cultureMuseum'] = 'culture_museum.png'
  output = feature_generic(bbox, 'Museum', 'cultureMuseum', 'tourism', 'museum', server)
  return output, myStyles
