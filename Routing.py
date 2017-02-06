

import numpy

LAT_DIM = 10000
LON_DIM = 20000
ALT_DIM = 8000


def tester():
    x = [5, 3, 4, 3, 1]
    mean, standard_dev = mean_with_standard_dev(x)
    print("mean: ", mean, "\n")
    print("standard deviation: ", standard_dev, "\n")

    return


# mean and standard deviation
def mean_with_standard_dev(x):
    mean = numpy.mean(x)
    standard_dev = numpy.std(x)

    return mean, standard_dev


def add_nofly_zones(graph):
    # set the defined regions as numpy.inf

    return graph


def add_weather_data(graph):

    return graph


def a_star(graph):

    return graph


def diff_from_direct(path_found):
    # get direct distance from database

    return


# grid-size in miles
def generate_graph(x_gridsize, y_gridsize, z_gridsize, use_weather, use_nofly):

    # create empty 2-D matrix (create altitude later)
    graph_3d = numpy.zeros(LAT_DIM/x_gridsize, LON_DIM/y_gridsize, ALT_DIM/z_gridsize)

    # populate graph with weather data
    if use_weather:
        graph_3d = add_weather_data(graph_3d)

    # populate graph with no-fly zones
    if use_nofly:
        graph_3d= add_nofly_zones(graph_3d)

    return graph_3d


def find_optimal_path():
    # # Temporary fill in for user inputs until that gets figured out # #
    x_gridsize = 10

    #enforce that x and y are of same length?
    y_gridsize = x_gridsize
    z_gridsize = 15

    use_weather = 0
    use_nofly = 1
    ################################################################

    gridmap = generate_graph(x_gridsize, y_gridsize, z_gridsize, use_weather, use_nofly)

    generated_optimal_path = a_star(gridmap, x_gridsize, y_gridsize)

    diff_from_direct(generated_optimal_path)

    return


tester()