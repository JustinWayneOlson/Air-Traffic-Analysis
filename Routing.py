

import numpy

# Specify the dimensions of the entire grid in miles. x,y, and altitude.
LAT_DIM = 10000
LON_DIM = 20000
ALT_DIM = 8000


#use to make up fake user data to test functions
def tester():
    x = [5, 3, 4, 3, 1]
    mean, standard_dev = mean_with_standard_dev(x)
    print("mean: ", mean, "\n")
    print("standard deviation: ", standard_dev, "\n")

    xy_gridsize = 1000
    use_weather = 1
    use_noflyzones = 1
    origin = "LA"
    destination = "NY"

    find_optimal_path(origin, destination, xy_gridsize, use_weather, use_noflyzones)


    return


# mean and standard deviation
def mean_with_standard_dev(x):
    mean = numpy.mean(x)
    standard_dev = numpy.std(x)

    return mean, standard_dev

def getCoords():
    x = numpy.random.random_integers(low = 0, high = LAT_DIM, size = 5)
    y = numpy.random.random_integers(low = 0, high = LON_DIM, size = 5)

    coords = x,y

    return coords


# could change add nofly zones and add weather data functions into one function and add an additional flag..
# should take in the coordinates of no fly data and map that to our grid indices
def add_nofly_zones(graph, xy_gridsize):
    # set the defined regions as numpy.inf
    x_coord, y_coord = getCoords()

    for i in range(0,len(x_coord)):
        x = int(numpy.floor(x_coord[i] / xy_gridsize))
        y = int(numpy.floor(y_coord[i] / xy_gridsize))
        graph[x, y] = numpy.inf

    return graph

# should take in the coordinates of weather data and map that to our grid indices
def add_weather_data(graph, xy_gridsize):
    # set the defined regions as numpy.inf
    x_coord, y_coord= getCoords()

    for i in range(0,len(x_coord)):
        x = int(numpy.floor(x_coord[i] / xy_gridsize))
        y = int(numpy.floor(y_coord[i] / xy_gridsize))

        graph[x, y] = numpy.inf


    return graph

def a_star(graph, origin, dest):

    return graph


def diff_from_direct(path_found):
    # get direct distance from database

    return


# grid-size in miles
def generate_graph(xy_gridsize, use_weather, use_nofly):

    # create empty 2-D matrix (create altitude as a later feature)
    graph_2d = numpy.zeros((int(numpy.floor(LAT_DIM/xy_gridsize)), int(numpy.floor(LON_DIM/xy_gridsize))))

    # populate graph with weather data
    if use_weather:
        graph_2d = add_weather_data(graph_2d, xy_gridsize)
    # populate graph with no-fly zones
    if use_nofly:
        graph_2d= add_nofly_zones(graph_2d, xy_gridsize)

    return graph_2d


def find_optimal_path(origin, dest, xy_gridsize, use_weather, use_nofly):

    gridmap = generate_graph(xy_gridsize, use_weather, use_nofly)

    # x and y grid square side size are same so don't need to pass in those
    generated_optimal_path = a_star(gridmap, origin, dest)

    diff_from_direct(generated_optimal_path)
    print(gridmap)


    return


tester()