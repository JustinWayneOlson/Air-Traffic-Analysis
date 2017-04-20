import json
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

def readDatabase(jobName):

	job = str(jobName)
	rows = None
	#connect to Cassandra cluster
	cluster = Cluster(["localhost"])
	session = cluster.connect()
	session.row_factory = dict_factory
	session.execute("USE AirportTrafficAnalytics")
	query = """SELECT * from Routing WHERE "jobName"=%s """ % (job)
	response = session.execute(query)
	
	print(response)

readDatabase("Route01")
