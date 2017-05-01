# -*- coding: utf-8 -*-
import numpy
import json
import collections
from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory
from cassandra.query import ordered_dict_factory
from cassandra.query import dict_factory
from copy import deepcopy

# Lat lon of Portal ND 48.9959° N, 102.5496° W
# Lat lon of Eureka calif 40.8021° N, 124.1637° W
# Homestead fl lat lon 25.4687° N, 80.4776° W
# cutler maine lat lon 44.6576° N, 67.2039° W

# Specify the dimensions of the entire grid in miles. x,y, and altitude in ft.
# need to fix Left and right Lon to be uniform with - format from front end
TOP_LAT = 48.9959 #Portal ND
BOT_LAT = 25.4687 #Homestead FL
LEFT_LON = 124.1637 #Eureka CA
RIGHT_LON = 50 #Cutler ME
miles_per_lat = 69
miles_per_lon = 69

LAT_DIM = TOP_LAT - BOT_LAT
LON_DIM = LEFT_LON - RIGHT_LON
ALT_DIM = 60000 # alt in ft

class Node:
	#add params like speed weather fuel etc
    def __init__(self, coords, lat, lon, alt):
        self.coords = coords
        #Node location and time
	self.lat = lat
        self.lon = lon
        self.alt = alt
	self.timeVisited = None

	#Aircraft Performance parameters
	self.aircraftType =  None
	self.aircraftWeight = None
	self.aircraftFuelWeight = None
	self.aircraftCargoWeight = None
	self.aircraftFuelUsage = None
	self.aircraftAirSpeed = None
	self.aircraftGrndSpeed = None

	#Weather parameters
	self.windSpeed = None
	self.windDirection = None
	self.precipitationChance = None
	self.precipitationType = None
	self.precipitationStrength = None
	self.airTemp = None
	self.humidity = None
	self.dewPoint = None

	#Airline parameters

	#A* parameters
        self.approxCost = 0
        self.neighbors = list()
        self.noFly = False
        self.weatherCost = 0
        self.parent = None
        self.priority = None
	self.nodeIndex = None

# function that translates lat,lon,alt to row column vblock indicies. Need to fix alt
def lat_lon_alt_to_grid(lat, lon, alt, grid_res_planar, grid_res_vert):
    num_rows, num_cols, num_vBlocks = get_num_blocks(grid_res_planar, grid_res_vert)
    row = int(((lat - (LAT_DIM / num_rows)/2) - BOT_LAT) / (LAT_DIM / num_rows))
    column = int(((lon - (LON_DIM / num_cols)/2) - RIGHT_LON) / (LON_DIM / num_cols))
    vblock = int(((alt - (ALT_DIM) / num_vBlocks)/2) / (ALT_DIM / num_vBlocks))
    result = [row, column, vblock]
    return result



def get_num_blocks(grid_res_planar, grid_res_vert):
    grid_res_planar = int(grid_res_planar)
    grid_res_vert = int(grid_res_vert)
    num_rows = int((LAT_DIM * miles_per_lat) / grid_res_planar)
    num_cols = int((LON_DIM * miles_per_lon )/ grid_res_planar)
    num_vBlocks = int(ALT_DIM / grid_res_vert)

    return num_rows, num_cols, num_vBlocks



def create_graph(grid_res_planar, grid_res_vert):
    num_rows, num_cols, num_vBlocks = get_num_blocks(grid_res_planar, grid_res_vert)


   # print("num_rows: ", num_rows)
   # print("num_cols: ", num_cols)
   # print("num_vBlocks: ", num_vBlocks)

    grid = []
    col_map = []
    alt_map = []
    for i in range(0,num_rows):
        for j in range(0,num_cols):
            for k in range(0,num_vBlocks):
                #lat = BOT_LAT + grid_res_planar * i + (grid_res_planar/2)
                #lon = RIGHT_LON + grid_res_planar * j + (grid_res_planar/2)
                #alt = grid_res_vert * k + (grid_res_vert/2)
                lat = BOT_LAT + (LAT_DIM/num_rows) * i + ((LAT_DIM/num_rows)/2)
                lon = RIGHT_LON + (LON_DIM / num_cols) * j + ((LON_DIM / num_cols) / 2)
                alt =  ALT_DIM/num_vBlocks * k + (ALT_DIM/num_vBlocks)/2
                alt_map.append(Node([i,j,k], lat, lon, alt))
            col_map.append(alt_map)
            alt_map = []
        grid.append(col_map)
        col_map = []

    for i in range(0, num_rows):
        for j in range(0, num_cols):
            for k in range(0, num_vBlocks):

                for a in range(-1, 2):
                    for b in range(-1, 2):
                        for c in range(-1, 2):
                            if(i+a >= 0 and i+a < num_rows and j+b >= 0 and j+b < num_cols and k+c >= 0 and k+c < num_vBlocks):
                                grid[i][j][k].neighbors.append(grid[i + a][j + b][k + c])

    return grid


def find_lowest_rank(openNodes):

    l_openNodes = len(openNodes)

    min_ranking = openNodes[0].priority
    min_index = 0

    for i in range(1,l_openNodes):
        if openNodes[i].priority < min_ranking:
            min_ranking = openNodes[i].priority
            min_index = i

    return min_index



def getDist(current, dest):
    dist = numpy.sqrt(numpy.square(current.lat - dest.lat) + numpy.square(current.lon - dest.lon) + numpy.square(current.alt - dest.alt))
    return dist


def three_dim_astar(origin, dest, grid_res_planar, grid_res_vert, heuristic):

    heuristicModule = __import__(heuristic)

    closedNodes = list()
    openNodes = list()

    grid = create_graph(grid_res_planar, grid_res_vert)
    currLoc = origin
    currNode = grid[origin[0]][origin[1]][origin[2]]
    currNode.priority = 0
    endNode = grid[dest[0]][dest[1]][dest[2]]

    openNodes.append(grid[origin[0]][origin[1]][origin[2]])


    while currLoc[0] != dest[0] or currLoc[1] != dest[1] or currLoc[2] != dest[2]:

        min_index = find_lowest_rank(openNodes)
        node_popped = openNodes.pop(min_index)
        closedNodes.append(node_popped)
        currNode = node_popped
        currLoc = [currNode.coords[0], currNode.coords[1], currNode.coords[2]]

        for neighNode in currNode.neighbors:

            cost = currNode.approxCost + getDist(currNode, neighNode)
            if openNodes.count(neighNode) == 1 and cost < neighNode.approxCost:
                openNodes.remove(neighNode)

            if closedNodes.count(neighNode) == 1 and cost < neighNode.approxCost:
                closedNodes.remove(neighNode)

            if openNodes.count(neighNode) == 0 and closedNodes.count(neighNode) == 0:
                neighNode.approxCost = cost
                openNodes.append(neighNode)
                neighNode.priority = neighNode.approxCost + heuristicModule.h(neighNode, endNode)
                neighNode.parent = currNode

    return grid


#Function That takes Origin and Dest identifyers and turns them in lat/lon
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
	#print("AirportLookup returned LatLonAlt", LatLonAlt)


	return LatLonAlt

#Function to be called from front end to perform routing calculation
#def routingDriver(jobName, Origin, Dest, gridResPlanar, gridResVert, heuristic):
def routingDriver(input_dict):
	jobName = input_dict['jobName']
	Origin = input_dict['Origin']
	Dest = input_dict['Dest']
	gridResPlanar = input_dict['gridResPlanar']
	gridResVert = input_dict['gridResVert']
	heuristic = input_dict['heuristic']

	source = airportlookup(Origin)
	target = airportlookup(Dest)
	OriginCoords = lat_lon_alt_to_grid(source[0], source[1], source[2], gridResPlanar, gridResVert)
	DestCoords = lat_lon_alt_to_grid(target[0], target[1], target[2],  gridResPlanar, gridResVert)

	#Origin and des are indicies for rows cols and vblocks
	grid = three_dim_astar(OriginCoords, DestCoords, gridResPlanar, gridResVert, heuristic)
	node = grid [DestCoords[0]] [DestCoords[1]] [DestCoords[2]]


	#routeLines to store route for database
	routeLines = {'links':[], 'nodes':[]}
	#NodeDict matches info in Node class to communicate with front end

	NodeDict = {'lat': float, 'long':float, 'alt': float, 'timeVisited': str, 'aircraftType': str, 'aircraftWeight': float, 'aircraftFuelWeight': float, 'aircraftCargoWeight': float, 'aircraftFuelUsage': float, 'aircraftAirSpeed': float, 'aircraftGrndSpeed': float, 'windSpeed': float, 'windDirection': float, 'precipitationChance': float, 'precipitationType': str, 'precipitationStrength': float, 'airTemp': float, 'humidity': float, 'dewPoint': float, 'weatherCost': float, 'nodeIndex': int}



	while(node.parent != None):
		#print("Coords: (%i, %i, %i)" % (node.parent.lat, node.parent.lon, node.parent.alt))

		#Add node class params to Node dict for front end visualization
		NodeDict['lat'] = node.parent.lat
		NodeDict['long'] = node.parent.lon * -1
		NodeDict['alt'] = node.parent.alt
		NodeDict['timeVisited'] = node.parent.timeVisited

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

		#A* parameters
        	NodeDict['noFly'] = node.parent.noFly
        	NodeDict['weatherCost'] =  node.parent.weatherCost
		NodeDict['nodeIndex'] = node.parent.nodeIndex

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

	return jobName
