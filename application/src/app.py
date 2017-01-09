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

#API endpoints are defined as classes

#Serve index.html
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #Patht to the webpage to be served
        self.render("./html/index.html")

#Get request takes in one arg via url and sends data back
class TestGetHandler(tornado.web.RequestHandler):
    def get(self, data):
        print("Serving JSON response to: " + data)
        #Convert passed in get request into int
        data=int(data)
        #Create dict to store data to return
        return_data={'response':[]}
        #Create random data
        '''Get data from database at this point'''
        for i in range(0,data):
            return_data['response'].append(random.random() * 10)
        #Write dict content to page, like a json response
        print return_data
        self.write(return_data)

class DisplayInfoHandler(tornado.web.RequestHandler):
    def flights_df(self, query):
        #Create Postgres engine
        POSTGRES_URL = "postgresql://test:pass@localhost:5432/airport_display"
        engine = create_engine(POSTGRES_URL)

        #Access vars from user query
        date_start = query['date_start']
        date_end = query['date_end']
        airport = query['airport']
        airline = query['airline']
        flight_num = query['flight_num']

        #Query Postgres DB
        if flight_num == "N/A":
            postgres_query = '''SELECT DISTINCT "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM "airplanes" WHERE 
                                "Origin" = '{0}' AND "Carrier" = '{1}' AND to_date("FlightDate", 'MM/DD/YYYY') >= to_date('{2}', 'MM/DD/YYYY') AND
                                to_date("FlightDate", 'MM/DD/YYYY') <= to_date('{3}', 'MM/DD/YYYY');'''.format(airport, airline, date_start, date_end)
        else:
            postgres_query = '''SELECT DISTINCT "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM "airplanes" WHERE 
                                "Origin" = '{0}' AND "Carrier" = '{1}' AND "FlightNum" = {2} AND to_date("FlightDate", 'MM/DD/YYYY') >= to_date('{3}', 'MM/DD/YYYY') AND
                                to_date("FlightDate", 'MM/DD/YYYY') <= to_date('{4}', 'MM/DD/YYYY');'''.format(airport, airline, flight_num, date_start, date_end)

        #Create/Return dataframe
        dataframe = pd.read_sql_query(postgres_query, con = engine)
        #MAYBE FIX THIS
        dataframe.fillna(0, inplace=True)

        return dataframe

    def airports_dict(self, filename):
        dataframe = pd.DataFrame.from_csv(filename)
        airports = {}

        for index, row in dataframe.iterrows():
            airports[row.Airport] = {}
            airports[row.Airport]["Lat"] = row.Lat
            airports[row.Airport]["Lon"] = row.Lon

        return airports

    def create_nodes(self, flights, airports):
        nodes = {}
        airports_list = []

        for index, row in flights.iterrows():
            dest_airport = str(row.Dest)
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

        nodes_list = []
        for key, val in nodes.iteritems():
            nodes_list.append(val)

        return nodes_list


    def post(self):
        received_query = json_decode(self.request.body)
        flights = self.flights_df(received_query)
        airports = self.airports_dict("data/airport_locs.csv")
        nodes = self.create_nodes(flights, airports)
        return_data = {}
        return_data['nodes'] = nodes
        print return_data
        self.write(return_data)

class DisplayAirportsHandler(tornado.web.RequestHandler):
    def create_flights(self):
        POSTGRES_URL = "postgresql://test:pass@localhost:5432/airport_display"
        engine = create_engine(POSTGRES_URL)
        dataframe = pd.read_sql_query('SELECT "Origin", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM "airplanes";', con = engine)
        return dataframe

    def read_airports(self, filename):
        dataframe = pd.DataFrame.from_csv(filename)
        return dataframe

    #Makes dictionary entries for each airport
    #Each airport has name, lat, long, delays, totals, etc.
    def create_airports(self, flights_df, airports_df):
        nodes = []
        airports = []
        for index, row in flights_df.iterrows():
            airport_code = str(row['Origin'])
            if airport_code == "SJU":
                airports.append(airport_code)
                continue
            if airport_code not in airports:
                airport = {}
                airport['Name'] = airport_code
                for index_, row_ in airports_df.iterrows():
                    if str(row_['Airport']) == airport_code:
                        airport['lat'] = float(row_['Lat'])
                        airport['long'] = float(row_['Lon'])
                        break

                airport['CarrierDelay'] = 0
                airport['WeatherDelay'] = 0
                airport['NASDelay'] = 0
                airport['SecurityDelay'] = 0
                airport['LateAircraftDelay'] = 0
                airport['TotalDelay'] = 0
                airport['TotalDelayedFlights'] = 0
                airport['TotalFlights'] = 0
                nodes.append(airport)
                airports.append(airport_code)

        return nodes

    def acc_delays(self, nodes, flights_df):
        flights_df.fillna(0, inplace=True)

        for index, row in flights_df.iterrows():
            CarrierDelay = int(row['CarrierDelay'])
            WeatherDelay = int(row['WeatherDelay'])
            NASDelay = int(row['NASDelay'])
            SecurityDelay = int(row['SecurityDelay'])
            LateAircraftDelay = int(row['LateAircraftDelay'])

            for node in nodes:
                if node['Name'] == str(row['Origin']):
                    cur_airport = node

            if CarrierDelay != 0 or WeatherDelay != 0 or NASDelay != 0 or SecurityDelay != 0 or LateAircraftDelay != 0:
                cur_airport['TotalDelayedFlights'] += 1

            cur_airport['CarrierDelay'] += int(row['CarrierDelay'])
            cur_airport['WeatherDelay'] += int(row['WeatherDelay'])
            cur_airport['NASDelay'] += int(row['NASDelay'])
            cur_airport['SecurityDelay'] += int(row['SecurityDelay'])
            cur_airport['LateAircraftDelay'] += int(row['LateAircraftDelay'])
            cur_airport['TotalDelay'] += int(row['CarrierDelay']) + int(row['WeatherDelay']) + int(row['NASDelay']) + int(row['SecurityDelay']) + int(row['LateAircraftDelay'])
            cur_airport['TotalFlights'] += 1

        return nodes

    def color(self, nodes):
        for node in nodes:
            avg = node['TotalDelay'] / node['TotalFlights']
            if avg < 5.0:
                node['Color'] = "green"
            elif avg >= 5.0 and avg < 15.0:
                node['Color'] = "yellow"
            else:
                node['Color'] = "red"

        return nodes

    def get(self):
        flights_df = self.create_flights()
        airports_df = self.read_airports("data/airport_locs.csv")
        airports = self.create_airports(flights_df, airports_df)
        nodes = self.acc_delays(airports, flights_df)
        nodes2 = self.color(nodes)
        for node in nodes2:
            print node
            print "\n"
        return_data = {}
        return_data['nodes'] = nodes2
        self.write(return_data)

#POST request takes in JSON from body, and returns JSON
class TestPostHandler(tornado.web.RequestHandler):
    def post(self):
        print(json_decode(self.request.body))
        return_data={
                'response':{
                    'message':'It Worked!!',
                    'content':random.random()*10
                }
        }
        self.write(return_data)

class D3TestHandler(tornado.web.RequestHandler):
    def get(self, city):
        city = city
        return_data = {}
        dataframe = create_dataframe(city)
        nodes = make_nodes(dataframe)
        links = make_links(nodes, city)
        return_data['nodes'] = nodes
        return_data['links'] = links

        self.write(return_data)


def create_dataframe(city):
        POSTGRES_URL = "postgresql://test:pass@localhost:5432/vis_test"
        engine = create_engine(POSTGRES_URL)
        dataframe = pd.read_sql_query('SELECT "OriginCityName", "Origin", "DestCityName", "Dest" FROM "airplanez" WHERE "OriginCityName" = \'' + city + '\';', con = engine)
        return dataframe

def coords(city):
    geolocator = Nominatim()
    location = geolocator.geocode(city)
    return location.latitude, location.longitude

def make_nodes(dataframe):
    nodes = []
    cities = []
    for index, row in dataframe.iterrows():
        if str(row['OriginCityName']) not in cities:
            airport = {}
            lat, lon = coords(str(row['OriginCityName']))
            airport['name'] = str(row['Origin'])
            airport['lat'] = lat
            airport['long'] = lon
            nodes.append(airport)
            cities.append(str(row['OriginCityName']))
        if str(row['DestCityName']) not in cities:
            airport = {}
            lat, lon = coords(str(row['DestCityName']))
            airport['name'] = str(row['Dest'])
            airport['lat'] = lat
            airport['long'] = lon
            nodes.append(airport)
            cities.append(str(row['DestCityName']))

    return nodes

def make_links(nodes, city):
    links = []
    origin_lat, origin_lon = coords(city)
    i = 0
    for node in nodes:
        if node['lat'] == origin_lat and node['long'] == origin_lon:
            origin = i
            break
        i += 1

    i = 0
    for node in nodes:
        if i == origin:
            i += 1
            continue
        else:
            link = {}
            link['source'] = origin
            link['target'] = i
            links.append(link)
            i += 1

    return links

#URL of endpoint, mapped to which class it correlates to
#URL is matched via regex
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        #localhost:8888/testget/(any number)
        (r"/test/", DisplayInfoHandler),
        (r"/display-airports", DisplayAirportsHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("serving on port 8888")
    tornado.ioloop.IOLoop.current().start()
