import GridMap as gm
import three_dim_astar

import numpy
import json
import collections
from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory
from cassandra.query import ordered_dict_factory
from cassandra.query import dict_factory
from copy import deepcopy

def airportlookup(identifier):
	#do a lookup on the Airport table on cassandra based on the identifyer and return the result as [lat, lon, alt] where each element is a double
	request = str(identifier)
	#Connect to cassandra cluster
	cluster = Cluster(["localhost"])
	session = cluster.connect()
	session.row_factory = named_tuple_factory  #ordered_dict_factory
	session.execute("USE AirportTrafficAnalytics")
	query = """SELECT "Lat", "Lon", "Alt" from AirportLocations  WHERE "Code"= '%s' """ % (request)
	rows = session.execute(query)
	response = rows[0]	

	#try  
	lat = float(response.Lat)
	lon = float(response.Lon)
	alt = float(response.Alt)
	lon = abs(lon)#remove this as soon as boundaries are properly set

	LatLonAlt =[lat, lon, alt]

def routingDriver(input_dict):
   jobName = input_dict['jobName']
   Origin = input_dict['Origin']
   Dest = input_dict['Dest']
   gridResPlanar = input_dict['gridResPlanar']
   gridResVert = input_dict['gridResVert']
   heuristic = input_dict['heuristic']
   bound_tol = input_dict['bound_tol'] //bound tol in degree lat lon
	
   source = airportlookup(Origin)
   target = airportlookup(Dest)
  
   myGridContainer = GridMapContainer(gridResPlanar,gridResVert, origin_lon = source[1], origin_lat = source[0], dest_lat= dest[0], dest_lon = dest[1], added_pt_buffer= 2, bound_tol = bound_tol)
   myGridContainer.make_graph()
   print("dims:")
   print(len(myGridContainer.gridMap[0]))
   print(len(myGridContainer.gridMap))
   # TODO its the order we are indexing... with alt
   grid = three_dim_astar([myGridContainer.gridMap], [source[2], source[1], source[0]], [target[2], target[1], target[0]], heuristic)
   node = grid [DestCoords[0]] [DestCoords[1]] [DestCoords[2]]


	#routeLines to store route for database
	routeLines = {'links':[], 'nodes':[]}
	#NodeDict matches info in Node class to communicate with front end

	NodeDict = {'lat': float, 'lon':float, 'alt': float, 'timeVisited': str, 'aircraftType': str, 'aircraftWeight': float, 'aircraftFuelWeight': float, 'aircraftCargoWeight': float, 'aircraftFuelUsage': float, 'aircraftAirSpeed': float, 'aircraftGrndSpeed': float, 'windSpeed': float, 'windDirection': float, 'precipitationChance': float, 'precipitationType': str, 'precipitationStrength': float, 'airTemp': float, 'humidity': float, 'dewPoint': float, 'weatherCost': float, 'nodeIndex': int}


	
	while(node.parent != None):
		#print("Coords: (%i, %i, %i)" % (node.parent.lat, node.parent.lon, node.parent.alt))
	
		#Add node class params to Node dict for front end visualization
		
            #A* Parameter
    		NodeDict['lat'] = node.parent.lat
		NodeDict['lon'] = node.parent.lon
		NodeDict['alt'] = node.parent.alt
   		NodeDict['noFly'] = node.parent.noFly
   		NodeDict['weatherCost'] =  node.parent.weatherCost
		NodeDict['timeVisited'] = node.parent.timeVisited
		NodeDict['nodeIndex'] = node.parent.nodeIndex
		
		#Aircraft Performance parameters
		NodeDict['aircraftType'] = node.parent.aircraftType
		NodeDict['aircraftWeight'] = node.parent.aircraftWeight
		NodeDict['aircraftFuelWeight'] = node.parent.aircraftFuelWeight
		NodeDict['aircraftCargoWeight'] = node.parent.aircraftCargoWeight
		NodeDict['aircraftFuelUsage'] = node.parent.aircraftFuelUsage
		NodeDict['aircraftAirSpeed'] = node.parent.aircraftAirSpeed
		NodeDict['aircraftGrndSpeed'] = node.parent.aircraftGrndSpeed
		
		#Weather parameters
		NodeDict['windSpeed'] = node.parent.windSpeed
		NodeDict['windDirection'] = node.parent.windDirection
		NodeDict['precipitationChance'] = node.parent.precipitationChance
		NodeDict['precipitationType'] = node.parent.precipitationType
		NodeDict['precipitationStrength'] = node.parent.precipitationStrength
		NodeDict['airTemp'] = node.parent.airTemp
		NodeDict['humidity'] = node.parent.humidity
		NodeDict['dewPoint'] = node.parent.dewPoint
		
		#Airline parameters
		

		
		#add Node dict values to routelines nodes and numbers to links for visualization.
		routeLines['nodes'].append(deepcopy(NodeDict))
		node = node.parent

	# write loop that takes length of nodes array and creates {source n target n+1} pairs for links in routeLines
	sourceTarget = {'source': int, 'target': int}
	linksIndex = 0
	
	for index in range(len(routeLines['nodes']) -1):
		sourceTarget['source']= linksIndex
		linksIndex += 1
		sourceTarget['target']= linksIndex
		routeLines['links'].append(deepcopy(sourceTarget))
	#print(routeLines)

	
	#connect to Cassandra Cluster
	cluster = Cluster(["localhost"])
	session = cluster.connect()
	session.row_factory = dict_factory
	#set Keyspace
	session.execute("USE AirportTrafficAnalytics")
	#set query format
	query = """INSERT INTO Routing ("jobName", "Origin", "Dest", "gridResPlanar", "gridResVert",
 "heuristic", "routeLines") VALUES (%s, %s, %s, %s, %s, %s, %s) """
	params = (str(jobName), str(Origin), str(Dest), int(gridResPlanar), int(gridResVert), str(heuristic), json.dumps(routeLines, "utf-8"))
	#In line above fix Origin and Dest to read user defined input not coords
	session.execute(query, params)

	return 1


