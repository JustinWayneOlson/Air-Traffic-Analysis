#VizTest.py
#Sample visualization

#RESULTS: https://plot.ly/~matt-oak/0/flights-from-chicago-il/

from geopy.geocoders import Nominatim
from sqlalchemy import create_engine
import plotly.plotly as py
py.sign_in('matt-oak', "APIKEY")
import pandas as pd
import psycopg2
import sys

POSTGRES_URL = "postgresql://test:pass@localhost:5432/vis_test"

def create_dataframe():
	engine = create_engine(POSTGRES_URL)
	dataframe = pd.read_sql_query('SELECT "OriginCityName", "DestCityName" FROM "airplanez" WHERE "OriginCityName" = \'Chicago, IL\';', con = engine)
	return dataframe

def get_coords(city):
	geolocator = Nominatim()
	location = geolocator.geocode(city)
	return location.latitude, location.longitude

def create_dicts(dataframe):
	origins = {}
	destinations = {}
	locs = {}

	for index, row in dataframe.iterrows():
		start = str(row['OriginCityName'])
		end = str(row['DestCityName'])
		if start not in origins:
			origins[start] = ("", "")
		if end not in destinations:
			destinations[end] = ("", "")

	for city in origins:
		lat, lon = get_coords(city)
		origins[city] = (lat, lon)

	for city in destinations:
		lat, lon = get_coords(city)
		destinations[city] = (lat, lon)

	return origins, destinations

def make_airports(origins, destinations):
	columns = ['name', 'lat', 'lon']
	df = pd.DataFrame(columns = columns)
	i = 0
	for city in origins:
		df.loc[i] = [city, origins[city][0], origins[city][1]]
		i += 1

	for city in destinations:
		df.loc[i] = [city, destinations[city][0], destinations[city][1]]
		i += 1
	
	return df

def make_flight_paths(origins, destinations):
	columns = ['start_lon', 'end_lon', 'start_lat', 'end_lat']
	df = pd.DataFrame(columns = columns)
	i = 0
	for city in destinations:
		df.loc[i] = [origins["Chicago, IL"][1], destinations[city][1], origins["Chicago, IL"][0], destinations[city][0]]
		i += 1
	
	return df



def viz(origins, destinations):
	airports = [ dict(
			type = "scattergeo",
			locationmode = "USA-states",
			lon = df_airports['lon'],
			lat = df_airports['lat'],
			hoverinfo = "text",
			text = df_airports["name"],
			mode = "markers",
			marker = dict(
				size = 2,
				color = "rgb(255, 0, 0)",
				line = dict(
					width = 3,
					color = "rgba(68, 68, 68, 0)"
				)
			))]

	flight_paths = []
	for i in range(len(df_flight_paths)):
		flight_paths.append(
			dict(
				type = "scattergeo",
				locationmode = "USA-states",
				lon = [df_flight_paths['start_lon'][i], df_flight_paths['end_lon'][i]],
				lat = [df_flight_paths['start_lat'][i], df_flight_paths['end_lat'][i]],
				mode = "lines",
				line = dict(
					width = 1,
					color = "red",
					),
				))

	layout = dict(
		title = "Flights from Chicago, IL",
		showlegend = False,
		geo = dict(
			scope = "north america",
			projection = dict(type = "azimuthal equal area"),
			showland = True,
			landcolor = "rgb(243, 243, 243)",
			countrycolor = "rgb(204, 204, 204)",
			),
		)

	fig = dict(data = flight_paths + airports, layout = layout)
	py.iplot(fig, filename = "flight paths")
	


dataframe = create_dataframe()
origins, destinations = create_dicts(dataframe)
df_airports = make_airports(origins, destinations)
df_flight_paths = make_flight_paths(origins, destinations)
viz(df_airports, df_flight_paths)