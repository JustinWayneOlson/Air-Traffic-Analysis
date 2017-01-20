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

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #Patht to the webpage to be served
        self.render("./html/index.html")

class DropdownFillHandler(tornado.web.RequestHandler):
   def get(self, column):
        POSTGRES_URL = "postgresql://postgres:postgres@localhost:5432/airports"
        engine = create_engine(POSTGRES_URL)
        query  = 'SELECT DISTINCT "{}" FROM flights LIMIT 100000'.format(column)
        dataframe = pd.read_sql_query(query, con = engine)
        response = {'response':[j for i in dataframe.values.tolist() for j in i]}
        self.write(response)

class DisplayFlightsHandler(tornado.web.RequestHandler):
    def post(self):
        received_query = json_decode(self.request.body)
        flights = flights_df(received_query)
        airports = airports_dict("data/airport_locs.csv")
        nodes, node_lookup = create_nodes(flights, airports)
        if len(nodes) == 1:
            self.write({"response":"Error no airports found for given query"})

        links = make_links(nodes, flights, node_lookup)
        return_data = {}
        return_data['nodes'] = nodes
        return_data['links'] = links
        nodes = color(nodes)
        self.write(return_data)

class DisplayAirportsHandler(tornado.web.RequestHandler):
    def post(self):
        received_query = json_decode(self.request.body)
        flights = flights_df(received_query)
        airports = airports_dict("data/airport_locs.csv")
        nodes, node_lookup = create_nodes(flights, airports)
        return_data = {}
        return_data['nodes'] = nodes
        nodes = color(nodes)
        self.write(return_data)

def flights_df(query):
  #Create Postgres engine
  POSTGRES_URL = "postgresql://postgres:postgres@localhost:5432/airports"
  engine = create_engine(POSTGRES_URL)
  #Access vars from user query
  where_string = ""
  for index,key in enumerate(query.keys()):
      if index == 0:
         where_string = " WHERE \"{}\" = '{}'".format(key, query[key])
      if index != 0:
         where_string += " AND \"{}\" = '{}'".format(key, query[key])
  limit_string = " LIMIT 100000;"
  query_string = 'SELECT DISTINCT "Origin", "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM "flights" {} {}'.format(where_string, limit_string)

  #Query Postgres DB
 # if flight_num == "N/A":
      #postgres_query = '''SELECT DISTINCT "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM "flights" WHERE
      #                    "Origin" = '{0}' AND "Carrier" = '{1}' AND to_date("FlightDate", 'MM/DD/YYYY') >= to_date('{2}', 'MM/DD/YYYY') AND
      #                    to_date("FlightDate", 'MM/DD/YYYY') <= to_date('{3}', 'MM/DD/YYYY') LIMIT 10;'''.format(airport, airline, date_start, date_end)
     # postgres_query = '''SELECT DISTINCT "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM "flights" WHERE
     #                     "Origin" b= '{0}' AND "Carrier" = '{1}'  LIMIT 10;'''.format(airport, airline, date_start, date_end)
  #else:
   #   postgres_query = '''SELECT DISTINCT "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM "flights" WHERE
   #                       "Origin" = '{0}' AND "Carrier" = '{1}' AND "FlightNum" = {2} AND to_date("FlightDate", 'MM/DD/YYYY') >= to_date('{3}', 'MM/DD/YYYY') AND
    #                      to_date("FlightDate", 'MM/DD/YYYY') <= to_date('{4}', 'MM/DD/YYYY') LIMIT 10;'''.format(airport, airline, flight_num, date_start, date_end)
  #Create/Return dataframe
  dataframe = pd.read_sql_query(query_string, con = engine)
  #MAYBE FIX THIS
  dataframe.fillna(0, inplace=True)
  return dataframe

def airports_dict(filename):
  dataframe = pd.DataFrame.from_csv(filename)
  airports = {}

  for index, row in dataframe.iterrows():
      airports[row.Airport] = {}
      airports[row.Airport]["Lat"] = row.Lat
      airports[row.Airport]["Lon"] = row.Lon

  return airports

def create_nodes(flights, airports):
  nodes = {}
  airports_list = []
  for index, row in flights.iterrows():
      dest_airport = str(row.Dest)
      origin_airport = str(row.Origin)
      #If we haven't encountered this airport before...
      if dest_airport not in airports_list:
          airport = {}
          airport["Name"] = dest_airport
          airport["lat"] = airports[dest_airport]["Lat"]
          airport["long"] = airports[dest_airport]["Lon"]
          airport["CarrierDelay"] = row.CarrierDelay
          if row.CarrierDelay > 0:
              airport["CarrierDelayTot"] = 1
          else:
              airport["CarrierDelayTot"] = 0
          airport["WeatherDelay"] = row.WeatherDelay
          if row.WeatherDelay > 0:
              airport["WeatherDelayTot"] = 1
          else:
              airport["WeatherDelayTot"] = 0
          airport["NASDelay"] = row.NASDelay
          if row.NASDelay > 0:
              airport["NASDelayTot"] = 1
          else:
              airport["NASDelayTot"] = 0
          airport["SecurityDelay"] = row.SecurityDelay
          if row.SecurityDelay > 0:
              airport["SecurityDelayTot"] = 1
          else:
              airport["SecurityDelayTot"] = 0
          airport["LateAircraftDelay"] = row.LateAircraftDelay
          if row.LateAircraftDelay > 0:
              airport["LateAircraftDelayTot"] = 1
          else:
              airport["LateAircraftDelayTot"] = 0
          airport["TotalDelay"] = row.CarrierDelay + row.WeatherDelay + row.NASDelay + row.SecurityDelay + row.LateAircraftDelay
          if airport["TotalDelay"] > 0:
              airport["TotalDelayedFlights"] = 1
          else:
              airport["TotalDelayedFlights"] = 0
          airport["TotalFlights"] = 1
          nodes[dest_airport] = airport
          airports_list.append(dest_airport)

      else:
          airport = nodes[dest_airport]
          airport["CarrierDelay"] += row.CarrierDelay
          if row.CarrierDelay > 0:
              airport["CarrierDelayTot"] += 1
          airport["WeatherDelay"] += row.WeatherDelay
          if row.WeatherDelay > 0:
              airport["WeatherDelayTot"] += 1
          airport["NASDelay"] += row.NASDelay
          if row.NASDelay > 0:
              airport["NASDelayTot"] += 1
          airport["SecurityDelay"] += row.SecurityDelay
          if row.SecurityDelay > 0:
              airport["SecurityDelayTot"] += 1
          airport["LateAircraftDelay"] += row.LateAircraftDelay
          if row.LateAircraftDelay > 0:
              airport["LateAircraftDelayTot"] += 1
          airport["TotalDelay"] += row.CarrierDelay + row.WeatherDelay + row.NASDelay + row.SecurityDelay + row.LateAircraftDelay
          if row.CarrierDelay + row.WeatherDelay + row.NASDelay + row.SecurityDelay + row.LateAircraftDelay > 0:
              airport["TotalDelayedFlights"] += 1
          airport["TotalFlights"] += 1
      airport['Color'] = ""

  nodes_lookup = {}
  nodes_list = [{'Color':'black', 'Name': origin_airport, 'lat': airports[origin_airport]['Lat'], 'long': airports[origin_airport]['Lon']}]
  nodes_lookup[origin_airport] = 0
  counter = 1
  for key, val in nodes.iteritems():
      nodes_list.append(val)
      nodes_lookup[val['Name']] = counter
      counter += 1
  return nodes_list, nodes_lookup

def color(nodes):
  for node in nodes:
      if node['Color'] == 'black':
         continue
      avg = node['TotalDelay'] / node['TotalFlights']
      if avg < 5.0:
          node['Color'] = "green"
      elif avg >= 5.0 and avg < 15.0:
          node['Color'] = "yellow"
      else:
          node['Color'] = "red"

  return nodes

def create_dataframe(city):
        POSTGRES_URL = "postgresql://postgres:postgres@localhost:5432/airports"
        engine = create_engine(POSTGRES_URL)
        dataframe = pd.read_sql_query('SELECT "OriginCityName", "Origin", "DestCityName", "Dest" FROM "airplanez" WHERE "OriginCityName" = \'' + city + '\';', con = engine)
        return dataframe

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

#URL of endpoint, mapped to which class it correlates to
#URL is matched via regex
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/js/(.*)",tornado.web.StaticFileHandler, {"path": "./static/js"},),
        (r"/css/(.*)",tornado.web.StaticFileHandler, {"path": "./static/css"},),
        (r"/display-airports", DisplayAirportsHandler),
        (r"/dropdown-fill/(.*)", DropdownFillHandler),
        (r"/display-flights", DisplayFlightsHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("serving on port 8888")
    tornado.ioloop.IOLoop.current().start()
