import json
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from routerizer import *



inputdict = {'Dest': 'LAX',  'Origin': 'SEA',  'gridResPlanar': '100',  'gridResVert': '1000',  'heuristic': '3dDistance',  'jobName': 'SeaDen', 'bound_tol': '1' }

routingDriver(inputdict)


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

def deleteFromDatabase(jobName):
	job =  str(jobName)
	
	cluster = Cluster(["localhost"])
	session = cluster.connect()
	session.row_factory = dict_factory
	session.execute("USE AirportTrafficAnalytics")
	query = """SELECT "jobName" from Routing """
	rows = session.execute(query)	
	print(list(rows))
	# turn the above line in an if to check if the route was found if true run the second querry below
	deleteQuery = """DELETE FROM Routing WHERE "jobName"= '%s' """ % (job)
	deleted = session.execute(deleteQuery)
	rows = session.execute(query)
	print(list(rows))


deleteFromDatabase("Job03")

#readDatabase("Route02")

#readDatabaseColumns()
