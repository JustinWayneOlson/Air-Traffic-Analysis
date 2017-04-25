#uses python 3.5
import csv
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

#File to import data from .dat file to .csv file. On;y writes airports in the USA with 3 letter codes
with open("airport_locations.dat", "r", encoding="utf8") as airports_in:
	#insert into Cassandra AirportLocations Table
	#connect to Cassandra Cluster
	cluster = Cluster(["localhost"])
	session = cluster.connect()
	session.row_factory = dict_factory
	#Set Keyspace
	session.execute("USE AirportTrafficAnalytics")
	#set query format
	query = """INSERT INTO AirportLocations ("City", "Code", "Lat", "Lon", "Alt") VALUES (%s, %s, %s, %s, %s) """
	#iterate through input file
	for line in airports_in:
		try:
			data = line.split(",")
			if ((data[3].replace("\"", "") == "United States") and (len(data[4].replace("\"", "")) > 1)):
				params = (data[2], data[4].replace("\"", ""), float(data[6]), float(data[7]), float(data[8]))
				#print("params: ", data[2], data[4].replace("\"", ""), float(data[6]), float(data[7]), float(data[8]))

				session.execute(query, params)
		except:
			print("Could not import airport num:", data[0])


