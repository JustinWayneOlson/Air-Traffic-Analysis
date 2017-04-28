import numpy
import GridMap

# Lat lon of Portal ND 48.9959° N, 102.5496° W
# Lat lon of Eureka calif 40.8021° N, 124.1637° W
# Homestead fl lat lon 25.4687° N, 80.4776° W
# cutler maine lat lon 44.6576° N, 67.2039° W

# Specify the dimensions of the entire grid in miles. x,y, and altitude.
TOP_LAT = 48.9959 #Portal ND
BOT_LAT = 25.4687 #Homestead FL
LEFT_LON = 124.1637 #Eureka CA
RIGHT_LON = 67.2039 #Cutler ME
miles_per_lat = 69
miles_per_lon = 69

LAT_DIM = TOP_LAT - BOT_LAT
LON_DIM = LEFT_LON - RIGHT_LON
ALT_DIM = 8000



class Node:

    def __init__(self, coords, lat, lon, alt, speed):
        self.coords = coords
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.speed = speed
        self.approxCost = 0
        self.neighbors = list()
        self.noFly = False
        self.weather_level = 0
        self.parent = None
        self.priority = None



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


# same as getDist for now until we figure out a better huristic
def h(current, dest):
    return getDist(current, dest)


def Astar_3D(grid, origin, dest):
    bounding_tol = 2 # in mies

    closedNodes = list()
    openNodes = list()

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
                neighNode.priority = neighNode.approxCost + h(neighNode, endNode, currNode)
                neighNode.parent = currNode

    return grid


def findShortestPath(grid_res_planar, grid_res_vert, origin, dest):
    grid = GridMap.GridMap(grid_res_planar,grid_res_vert, origin, dest)
    Astar_3D(grid, origin, dest)


grid = Astar_3D([0,5,1], [0,15,8])

node = grid[0][15][8]

while(node.parent != None):
    print("Coords: (%i, %i, %i)" % (node.parent.lat, node.parent.lon, node.parent.alt))
    node = node.parent
