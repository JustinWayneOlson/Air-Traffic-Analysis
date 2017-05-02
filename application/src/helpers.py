from __future__ import division
from geopy.geocoders import Nominatim
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import numpy as np
import sys
import json
import tornado.ioloop
import tornado.web
from  tornado.escape import json_decode
import random
import os
import pprint as pp
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import copy

def cql_query(query_string, cols):
  print query_string
  #Connect to the Cassandra database
  cluster = Cluster(["localhost"])
  session = cluster.connect()
  session.execute("USE AirportTrafficAnalytics")
  print query_string
  rows = session.execute(query_string)
  #Initialize Dataframe
  df = pd.DataFrame(columns=cols)
  #Insert rows from query response
  i = 0
  df_index = 0
  while True:
    try:
      row = np.array(rows[i])
      print(row)
      if(not((df == row).all(1).any())):
        print(type(row))
        df.loc[df_index] = row
        df_index += 1
      i += 1
    except IndexError:
      break
  #TODO Dataframe and distinct
  return df

def cql_query_dict(query):
   cluster = Cluster(["localhost"])
   session = cluster.connect()
   session.row_factory = dict_factory
   session.execute("USE AirporttrafficAnalytics")
   request = query
   rows = session.execute(request)
   return rows


#Method to create Pandas dataframe with flight information
def flights_df(query):

  #Construct the database query based upon user-input
  where_string = ""
  start_date = False
  end_date = False
  verbose_toggle = query['verbose_toggle']
  del query['verbose_toggle']
  paths_toggle = query['path_toggle']
  del query['path_toggle']

  if "date_start" in query.keys():
      date_start = ' AND to_date("FlightDate", \'YYYY-MM-DD\') >= to_date(\'{}\', \'MM/DD/YYYY\')'.format(query["date_start"])
      start_date = True
      del  query["date_start"]
  if "date_end" in query.keys():
      date_end = ' AND to_date("FlightDate", \'YYYY-MM-DD\') <= to_date(\'{}\', \'MM/DD/YYYY\')'.format(query["date_end"])
      end_date = True
      del query["date_end"]
  for index,key in enumerate(query.keys()):
      if index == 0:
           item = str(query[key]).replace('[','(').replace(']',')').replace("u'","'")
           print item
           where_string = " WHERE \"{}\" IN {}".format(key, item)
      if index != 0:
           item = str(query[key]).replace('[','(').replace(']',')').replace("u'","'")
           print item
           where_string += " AND \"{}\" IN {}".format(key, item)
  if(start_date):
      where_string += date_start
  if(end_date):
    where_string += date_end
  limit_string = " LIMIT 100000 ALLOW FILTERING;"
  query_string = 'SELECT "FlightDateString", "Origin", "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM AirportTrafficAnalytics.Transtats {} {}'.format(where_string, limit_string)
  print query_string

  #Create and return dataframe
  cols = ['FlightDateString', 'Origin', 'Dest', 'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
  dataframe = cql_query(query_string, cols)
  dataframe.fillna(0, inplace=True)
  return dataframe, verbose_toggle, paths_toggle

#Method to create 'airports' dictionary of dictionaries where key = airport code and values = lat/lon
def airports_dict(filename):
  dataframe = pd.DataFrame.from_csv(filename)
  airports = {}

  for index, row in dataframe.iterrows():
      airports[row.Airport] = {}
      airports[row.Airport]["Lat"] = row.Lat
      airports[row.Airport]["Lon"] = row.Lon

  return airports

#Method to create 'nodes' dictionary of dictionaries consisting of airport delay information
def create_nodes(flights, airports):
  nodes = {}
  airports_list = []

  #Iterate through the flights information Pandas dataframe
  for index, row in flights.iterrows():
      dest_airport = str(row.Dest)
      origin_airport = str(row.Origin)

      #If we haven't encountered this airport before initialize all the values accordingly
      if dest_airport not in airports_list:
          airport = {}
          carrier_delay = int(float(row.CarrierDelay))
          weather_delay = int(float(row.WeatherDelay))
          nas_delay = int(float(row.NASDelay))
          security_delay = int(float(row.SecurityDelay))
          late_delay = int(float(row.LateAircraftDelay))
          airport["Name"] = dest_airport
          airport["lat"] = airports[dest_airport]["Lat"]
          airport["long"] = airports[dest_airport]["Lon"]
          airport["CarrierDelay"] = carrier_delay
          if row.CarrierDelay > 0:
              airport["CarrierDelayTot"] = 1
          else:
              airport["CarrierDelayTot"] = 0
          airport["WeatherDelay"] = weather_delay
          if row.WeatherDelay > 0:
              airport["WeatherDelayTot"] = 1
          else:
              airport["WeatherDelayTot"] = 0
          airport["NASDelay"] = nas_delay
          if row.NASDelay > 0:
              airport["NASDelayTot"] = 1
          else:
              airport["NASDelayTot"] = 0
          airport["SecurityDelay"] = security_delay
          if row.SecurityDelay > 0:
              airport["SecurityDelayTot"] = 1
          else:
              airport["SecurityDelayTot"] = 0
          airport["LateAircraftDelay"] = late_delay
          if row.LateAircraftDelay > 0:
              airport["LateAircraftDelayTot"] = 1
          else:
              airport["LateAircraftDelayTot"] = 0
          airport["TotalDelay"] = carrier_delay + weather_delay + nas_delay + security_delay + late_delay
          if airport["TotalDelay"] > 0:
              airport["TotalDelayedFlights"] = 1
          else:
              airport["TotalDelayedFlights"] = 0
          airport["TotalFlights"] = 1
          nodes[dest_airport] = airport
          airports_list.append(dest_airport)

      #Otherwise accumulate delay information
      else:
          airport = nodes[dest_airport]
          carrier_delay = int(float(row.CarrierDelay))
          weather_delay = int(float(row.WeatherDelay))
          nas_delay = int(float(row.NASDelay))
          security_delay = int(float(row.SecurityDelay))
          late_delay = int(float(row.LateAircraftDelay))
          print "airport"
          print type(airport['CarrierDelay'])
          print "var"
          print type(carrier_delay)
          airport["CarrierDelay"] += carrier_delay
          if carrier_delay > 0:
              airport["CarrierDelayTot"] += 1
          airport["WeatherDelay"] += weather_delay
          if weather_delay > 0:
              airport["WeatherDelayTot"] += 1
          airport["NASDelay"] += nas_delay
          if nas_delay > 0:
              airport["NASDelayTot"] += 1
          airport["SecurityDelay"] += security_delay
          if security_delay > 0:
              airport["SecurityDelayTot"] += 1
          airport["LateAircraftDelay"] += late_delay
          if late_delay > 0:
              airport["LateAircraftDelayTot"] += 1
          airport["TotalDelay"] += carrier_delay + weather_delay + nas_delay + security_delay + late_delay
          if carrier_delay + weather_delay + nas_delay + security_delay + late_delay > 0:

              airport["TotalDelayedFlights"] += 1
          airport["TotalFlights"] += 1
      airport['Color'] = ""

  #Assign unique, numeric values to each airport
  nodes_lookup = {}
  nodes_list = [{'Color':'white', 'Name': origin_airport, 'lat': airports[origin_airport]['Lat'], 'long': airports[origin_airport]['Lon']}]
  nodes_lookup[origin_airport] = 0
  counter = 1
  for key, val in nodes.iteritems():
      nodes_list.append(val)
      nodes_lookup[val['Name']] = counter
      counter += 1
  return nodes_list, nodes_lookup

#Method to assign colors to nodes on the Google map
def color(nodes):
  for node in nodes:

      #Force origin airport to be colored white
      if node['Color'] == 'white':
         continue
      avg = node['TotalDelay'] / node['TotalFlights']
      print avg
      #If average >90% --> red
      if avg > 75:
          node['Color'] = "red"

      #Elif average <90% and >80% --> yellow
      elif avg >= 50 and avg < 75:
          node['Color'] = "yellow"

      #Else --> green
      else:
          node['Color'] = "green"

  return nodes

#Method to construct links between airports
def make_links(nodes, flights, node_lookup):
    links = []
    temp_dict = {}
    targets = []
    for index,row in flights.iterrows():
        print node_lookup[row.Dest]
        temp_dict['source'] = node_lookup[row.Origin]
        temp_dict['target'] = node_lookup[row.Dest]
        if(not(row.Dest in targets)):
            links.append(temp_dict)
            targets.append(row.Dest)
        temp_dict = {}
    print links

    return links
