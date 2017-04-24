import json
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

# returns list of jobs
jobNames = """SELECT "jobName" from Routing """









def readDatabaseColumns():
	
	#connect to Cassandra cluster
	cluster = Cluster(["localhost"])
	session = cluster.connect()
	session.row_factory = dict_factory
	session.execute("USE AirportTrafficAnalytics")
	query = jobNames
	rows = session.execute(query)
	response = rows[0]	
	print(response)



def readDatabase(jobName):

	job = str(jobName)
	#connect to Cassandra cluster
	cluster = Cluster(["localhost"])
	session = cluster.connect()
	session.row_factory = dict_factory
	session.execute("USE AirportTrafficAnalytics")
	query = """SELECT * from Routing WHERE "jobName"= '%s' """ % (job)
	rows = session.execute(query)
	response = rows[0]	
	print(response)

#readDatabase("Route01")

readDatabaseColumns()
