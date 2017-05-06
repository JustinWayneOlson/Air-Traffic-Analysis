
import Routing as f_route
import Analysis as f_analys
import unittest as test
import numpy as np


'''documentation for unittest HERE: https://docs.python.org/2/library/unittest.html

    Notes:
    Just add this to a project, include proper files you want to test, and create tests accordingly.
    Obviously no need to change anything about your code (the code will still run like normal except have extra test report at end)
    The test output is listed by test function alphabetically.
    If one test fails, the rest will still execute.

'''

class RoutingTests(test.TestCase):

    # first way of checking array is equal
    def test_coords_to_inf2(self):
        m = [1,2,3]
        n = [3,2,4]
        test_matrix = np.zeros((4,5))
        self.assertIsNone(np.testing.assert_array_equal((f_route.set_squares_to_inf(test_matrix, m, n, 1))[0,:], np.zeros((5))))


    # second way of checking array is equal (http://stackoverflow.com/questions/3302949/whats-the-best-way-to-assert-for-numpy-array-equality)
    def test_coords_to_inf(self):
        m = [70, 100, 120]
        n = [30,35,40]
        test_matrix = np.zeros((4, 5))
        test_matrix_ans = np.zeros((4,5))
        test_matrix_ans[1,3] = np.inf
        test_matrix_ans[2, 2] = np.inf
        test_matrix_ans[3, 4] = np.inf
        self.assertEqual((f_route.set_squares_to_inf(test_matrix, m, n, 1)).tolist(), test_matrix_ans.tolist() )


    # demonstrates what happens when a unit test fails
    def test_coords_to_inf3(self):
        m = [1, 2, 3]
        n = [3, 2, 4]
        test_matrix = np.zeros((4, 5))
        self.assertTrue(False)


    # third way of checking array is equal (http://stackoverflow.com/questions/3302949/whats-the-best-way-to-assert-for-numpy-array-equality)
    def test_coords_to_inf4(self):
        m = [1,2,3]
        n = [3,2,4]
        test_matrix = np.zeros((4, 5))
        test_matrix_ans = np.zeros((4,5))
        test_matrix_ans[1,3] = np.inf
        test_matrix_ans[2, 2] = np.inf
        test_matrix_ans[3, 4] = np.inf
        self.assertTrue(((f_route.set_squares_to_inf(test_matrix, m, n, 1)) == test_matrix_ans).all() )

    def test_generate_graph(self):

        test_matrix = np.zeros((4, 5))
        test_matrix_ans = np.zeros((4,5))
        test_matrix_ans[1,3] = np.inf
        test_matrix_ans[2, 2] = np.inf
        test_matrix_ans[3, 4] = np.inf
        self.assertTrue(((f_route.generate_graph(1, 1, 0)) == test_matrix_ans).all() )




#from unittest site (allows for more verbose output to console)
suite = test.TestLoader().loadTestsFromTestCase(RoutingTests)
test.TextTestRunner(verbosity=2).run(suite)
