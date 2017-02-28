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

#Handler for main (index) page
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #URL to main (index) page
        self.render("./html/index.html")

#Handler for about page
class AboutHandler(tornado.web.RequestHandler):
  def get(self):
      #URL to about page
      self.render("./html/about.html")

#Handler to populate dropdown menus with options from database
class DropdownFillHandler(tornado.web.RequestHandler):
   def get(self, column):
        POSTGRES_URL = "postgresql://postgres:postgres@localhost:5432/airports"
        engine = create_engine(POSTGRES_URL)
        query  = 'SELECT DISTINCT "{}" FROM flights LIMIT 100000'.format(column)
        dataframe = pd.read_sql_query(query, con = engine)
        response = {'response':[j for i in dataframe.values.tolist() for j in i]}
        self.write(response)

#Handler to display airports (nodes) and flights (links)
class DisplayAirportsHandler(tornado.web.RequestHandler):
    def post(self):
        received_query = json_decode(self.request.body)
        flights, verbose_toggle, paths_toggle = flights_df(received_query)
        return_data = {}
        if(verbose_toggle):
           return_data['verbose'] = "This is eventually going to be more information!"
        print(paths_toggle)
        print(type(paths_toggle))
        if(paths_toggle):
            airports = airports_dict("data/airport_locs.csv")
            nodes, node_lookup = create_nodes(flights, airports)
            if len(nodes) == 1:
                self.write({"response":"Error no airports found for given query"})

            links = make_links(nodes, flights, node_lookup)
            return_data['nodes'] = nodes
            return_data['links'] = links
            nodes = color(nodes)
            self.write(return_data)
        else:
            airports = airports_dict("data/airport_locs.csv")
            nodes, node_lookup = create_nodes(flights, airports)
            return_data['nodes'] = nodes
            nodes = color(nodes)
            pp.pprint(return_data)
            self.write(return_data)

#Method to create Pandas dataframe with flight information
def flights_df(query):
  #Connect to the PostgreSQL database
  POSTGRES_URL = "postgresql://postgres:postgres@localhost:5432/airports"
  engine = create_engine(POSTGRES_URL)

  #Construct the PostgreSQL query based upon user-input
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
  limit_string = " LIMIT 100000;"
  query_string = 'SELECT DISTINCT "Origin", "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM "flights" {} {}'.format(where_string, limit_string)
  print query_string


  #Create and return dataframe
  dataframe = pd.read_sql_query(query_string, con = engine)
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

      #Otherwise accumulate delay information
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

#URL of endpoint, mapped to which class it correlates to
#URL is matched via regex
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/about", AboutHandler),
        (r"/js/(.*)",tornado.web.StaticFileHandler, {"path": "./static/js"},),
        (r"/css/(.*)",tornado.web.StaticFileHandler, {"path": "./static/css"},),
        (r"/img/(.*)",tornado.web.StaticFileHandler, {"path": "./static/img"},),
        (r"/display-airports", DisplayAirportsHandler),
        (r"/dropdown-fill/(.*)", DropdownFillHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("serving on port 8888")
    tornado.ioloop.IOLoop.current().start()
