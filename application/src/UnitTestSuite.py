
import RoutingOO as routing
import AStar as astar
import unittest as test
import numpy as np
import GridMap as gm

'''documentation for unittest HERE: https://docs.python.org/2/library/unittest.html

    Notes:
    Just add this to a project, include proper files you want to tests, and create tests accordingly.
    Obviously no need to change anything about your code (the code will still run like normal except have extra test report at end)
    The test output is listed by test function alphabetically.
    If one test fails, the rest will still execute.

'''

class RoutingTests(test.TestCase):

    def test_grid_map_init_test(self):
        self.assertTrue(1 == 1)

    def test_grid_map_init_coods(self):

        myGrid = gm.GridMapContainer(planar_res = .2, alt_res = 500000, bound_tol = 2, added_pt_buffer = 0.02, origin_lat = 30, origin_lon = 40, dest_lat = 50, dest_lon = 80)


        self.assertTrue(myGrid.start_lat == 29.98)
        self.assertTrue(myGrid.end_lat  == 50.02)
        self.assertTrue(myGrid.start_lon == 39.98)
        self.assertTrue(myGrid.end_lon == 80.02)
        self.assertTrue(myGrid.lat_dim == 20.04)
        self.assertTrue(myGrid.lon_dim == 40.04)
        self.assertTrue(myGrid.is_lon_major_axis == True)
        self.assertTrue(myGrid.major_axis_sign == 1)
        self.assertTrue(myGrid.minor_axis_sign == 1)

    def test_grid_map_init_coods2(self):
        myGrid = gm.GridMapContainer(planar_res=.2, alt_res=500000, bound_tol=2, added_pt_buffer=0.02,
                                     origin_lon=50, origin_lat=80, dest_lon=30, dest_lat=40)

        self.assertTrue(myGrid.end_lon == 29.98)
        self.assertTrue(myGrid.start_lon == 50.02)
        self.assertTrue(myGrid.end_lat == 39.98)
        self.assertTrue(myGrid.start_lat == 80.02)
        self.assertTrue(myGrid.lon_dim == 20.04)
        self.assertTrue(myGrid.lat_dim == 40.04)
        self.assertTrue(myGrid.is_lon_major_axis == False)
        self.assertTrue(myGrid.major_axis_sign == -1)
        self.assertTrue(myGrid.minor_axis_sign == -1)


    def test_grid_map_init_coods3(self):
        myGridContainer = gm.GridMapContainer(planar_res=.2, alt_res=500000, bound_tol=2, added_pt_buffer=0.02,
                                     origin_lat=50, origin_lon=80, dest_lat=30, dest_lon=40)


        self.assertTrue(myGridContainer.end_lat == 29.98)
        self.assertTrue(myGridContainer.start_lat == 50.02)
        self.assertTrue(myGridContainer.end_lon == 39.98)
        self.assertTrue(myGridContainer.start_lon == 80.02)
        self.assertTrue(myGridContainer.lat_dim == 20.04)
        self.assertTrue(myGridContainer.lon_dim == 40.04)
        self.assertTrue(myGridContainer.is_lon_major_axis == True)
        self.assertTrue(myGridContainer.major_axis_sign == -1)
        self.assertTrue(myGridContainer.minor_axis_sign == -1)

        myGridContainer.make_graph()

        self.assertTrue(myGridContainer.offsets[0] == 0)

#def test_with_Astar(self):


    #findShortestPath(grid_res_planar = .2, grid_res_vert = 500000, origin = [50,80,1], dest = [30,40,1], added_pt_buffer = 0.01, bound_tol = 2)




#from unittest site (allows for more verbose output to console)
suite = test.TestLoader().loadTestsFromTestCase(RoutingTests)
test.TextTestRunner(verbosity=2).run(suite)