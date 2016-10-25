from geopy.geocoders import Nominatim
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import sys
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
    POSTGRES_URL = "postgresql://test:pass@localhost:5432/vis_test"

    def create_dataframe(city):
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
                airport['lon'] = lon
                nodes.append(airport)
                cities.append(str(row['OriginCityName']))
            if str(row['DestCityName']) not in cities:
                airport = {}
                lat, lon = coords(str(row['DestCityName']))
                airport['name'] = str(row['Dest'])
                airport['lat'] = lat
                airport['lon'] = lon
                nodes.append(airport)
                cities.append(str(row['DestCityName']))

        return nodes

    def make_links(nodes, city):
        links = []
        origin_lat, origin_lon = coords(city)
        i = 0
        for node in nodes:
            if node['lat'] == origin_lat and node['lon'] == origin_lon:
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

    def get(self, city):
        city = city
        return_data = {}
        dataframe = create_dataframe(city)
        nodes = make_nodes(dataframe)
        links = make_links(nodes, city)
        return_data['nodes'] = nodes
        return_data['links'] = links

        self.write(return_data)



#URL of endpoint, mapped to which class it correlates to
#URL is matched via regex
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        #localhost:8888/testget/(any number)
        (r"/testget/([0-9]*)", TestGetHandler),
        (r"/testd3/(.*)", D3TestHandler),
        (r"/testpost", TestPostHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("serving on port 8888")
    tornado.ioloop.IOLoop.current().start()
