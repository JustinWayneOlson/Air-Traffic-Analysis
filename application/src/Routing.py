# Referenced http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html for this implementation

import numpy
import sys
import matplotlib.pyplot as plt

# Lat lon of Portal ND 48.9959° N, 102.5496° W
# Lat lon of Eureka calif 40.8021° N, 124.1637° W
# Homestead fl lat lon 25.4687° N, 80.4776° W
# cutler maine lat lon 44.6576° N, 67.2039° W

# Specify the dimensions of the entire grid in miles. x,y, and altitude.
TOP_LAT = 48.9959 #Portal ND
BOT_LAT = 25.4687 #Homestead FL
LEFT_LON = 124.1637 #Eureka CA
RIGHT_LON = 67.2039 #Cutler ME


LAT_DIM = TOP_LAT - BOT_LAT
LON_DIM = LEFT_LON - RIGHT_LON
ALT_DIM = 8000

#http://stackoverflow.com/questions/28242917/numpy-array-to-graph
def coordsValid(lat_coords, lon_coords):
    if (len(lat_coords) != len(lon_coords)):
        return False
    for i in range(1,len(lat_coords)):
        if (lat_coords[i] > TOP_LAT | lat_coords[i] < BOT_LAT):
            return False
        if (lon_coords[i] > LEFT_LON | lon_coords[i] < RIGHT_LON):
            return False
    return True





def getCoords():
    x = numpy.random.random_integers(low = 0, high = LAT_DIM, size = 5)
    y = numpy.random.random_integers(low = 0, high = LON_DIM, size = 5)

    lat = [30, 35, 40]
    lon = [70, 100, 120]

    coords = lat, lon

    print("hola")
    return coords


def set_squares_to_inf(graph, lat_coords, lon_coords, latlon_gridsize):

    for i in range(0,len(lat_coords)):
        # adjust coord for grid
        m = lat_coords[i] - BOT_LAT
        n = lon_coords[i] - RIGHT_LON
        m = int(numpy.floor(m / latlon_gridsize))
        n = int(numpy.floor(n / latlon_gridsize))
        #prob need to change between py 2 and py 3

        print(m, n)
        graph[m, n] = numpy.inf

    return graph


# could change add nofly zones and add weather data functions into one function and add an additional flag..
# should take in the coordinates of no fly data and map that to our grid indices
def add_nofly_zones(graph, xy_gridsize):

    x_coords, y_coords = getCoords()
    if(coordsValid()):
        set_squares_to_inf(graph, x_coords, y_coords, xy_gridsize)

    return graph


# should take in the coordinates of weather data and map that to our grid indices
def add_weather_data(graph, xy_gridsize):

    x_coords, y_coords = getCoords()
    set_squares_to_inf(graph, x_coords, y_coords, xy_gridsize)

    return graph


def remove_lowest(graph, nodes_to_visit):
    l_nodes_to_visit = (nodes_to_visit.shape)[0]
    min = graph[nodes_to_visit[0][0], nodes_to_visit[0][1]]
    min_index = 0
    for i in range(0,l_nodes_to_visit):
        size = graph[nodes_to_visit[i][0], nodes_to_visit[i][1]]
        if(size < min):
            min = size
            min_index = i
    print(min_index)
    graph_index = (nodes_to_visit[min_index][0], nodes_to_visit[min_index][1])
    nodes_to_visit = numpy.delete(nodes_to_visit, min_index, 0)
    print(nodes_to_visit)

    return [graph_index, nodes_to_visit]

def get_neighbor_index(neigh, currLoc, dims):
    y = currLoc[0]
    x = currLoc[1]
    end_y = dims[0] - 1
    end_x = dims[1] - 1
    dist = numpy.inf
    # up and left
    if neigh == 0 and x != 0 and y != 0:
        neigh_coords = [x-1, y-1]
        dist = numpy.sqrt(2)
    # up
    elif neigh == 1 and y != 0:
        neigh_coords = [x, y - 1]
        dist = 1
    # up and right
    elif neigh == 2 and y != 0 and x != end_x:
        neigh_coords = [x + 1, y - 1]
        dist = numpy.sqrt(2)
    # right
    elif neigh == 3 and x != end_x:
        neigh_coords = [x + 1, y]
        dist = 1
    # right and down
    elif neigh == 4 and x != end_x and y != end_y:
        neigh_coords = [x + 1, y + 1]
        dist = numpy.sqrt(2)
    # down
    elif neigh == 5 and y != end_y:
        neigh_coords = [x, y + 1]
        dist = 1
    # down and left
    elif neigh == 6 and y != end_y and x != 0:
        neigh_coords = [x - 1, y + 1]
        dist = numpy.sqrt(2)
    # left
    elif neigh == 7 and x != 0:
        neigh_coords = [x - 1, y]
        dist = 1

    return neigh_coords, dist

def get_index_num(neigh_index, graph_dims):
    return(neigh_index[0] * graph_dims[1] + neigh_index[1])


def a_star(graph, origin, dest):
    dims = graph.shape()
    parent_graph = numpy.zeros(dims)

    #set the distance at the origin node to zero
    graph[origin[0], origin[1]] = 0
    currLoc = origin
    nodes_to_visit = {[origin[0], origin[1]]}
    nodes_done = {[origin[0], origin[1]]}
    nodes_done.remove(origin)




# need to store the cost of getting to a node somewhere
    # there will be one extra loop here that removes the origin and sets it to our current location
    while(currLoc != dest):
        (currLoc, nodes_to_visit, visited, to_neigh_dist) = remove_lowest(graph, nodes_to_visit, visited)
        for i in range(0, 8):
            currCost = graph[currLoc] + to_neigh_dist
            neigh_index = get_neighbor_index(i, currLoc, dims)
            if (numpy.any(nodes_to_visit == neigh_index) and currCost < graph[neigh_index]):
                nodes_to_visit.remove(neigh_index)
            if (numpy.any(nodes_done == neigh_index) and currCost < graph[neigh_index]):
                nodes_done.remove(neigh_index)
            if (numpy.all(nodes_to_visit != neigh_index) and numpy.all(nodes_done != neigh_index)):
                graph[neigh_index] = currCost
                nodes_to_visit.add(neigh_index)
                parent_graph[currLoc] = get_index_num(neigh_index, dims)



    return graph



# huristic for A*
def h(graph, curr_node, end_node):
    # get direct distance from database
    lat_curr, lon_curr = graph[curr_node]
    lat_end, lon_end = graph[end_node]

    eucl_dist = numpy.sqrt(numpy.sqare(lat_curr - lat_end) + numpy.square(lon_curr - lat_curr))

    return eucl_dist


# grid-size in miles
def generate_graph(xy_gridsize, use_weather, use_nofly):

    # create empty 2-D matrix (create altitude as a later feature)
    x_dim = int(numpy.ceil(LAT_DIM/xy_gridsize))
    y_dim = int(numpy.ceil(LON_DIM/xy_gridsize))
    print('x_dim:', x_dim)
    print('y_dim:', y_dim)

    graph_2d = numpy.zeros((x_dim, y_dim))

    # populate graph with weather data
    if use_weather:
        graph_2d = add_weather_data(graph_2d, xy_gridsize)
    # populate graph with no-fly zones
    if use_nofly:
        graph_2d= add_nofly_zones(graph_2d, xy_gridsize)
    #plt.show(block=True)
    #plt.plot(2,3)
    plt.matshow(graph_2d)
    plt.show()
    #



    return graph_2d

'''
def find_optimal_path(origin, dest, xy_gridsize, use_weather, use_nofly):

    gridmap = generate_graph(xy_gridsize, use_weather, use_nofly)

    # x and y grid square side size are same so don't need to pass in those
    generated_optimal_path = a_star(gridmap, origin, dest)

    diff_from_direct(generated_optimal_path)

    return 9

generate_graph(1, 1, 0)
'''
