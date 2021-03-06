'''
Created on 19/03/2014

@author: mmpe
'''
import unittest


import numpy as np
from functions.matrix import solvers
A = np.array([[2, 1, 1], [1, 1, -1], [1, 1, 3]])
b = np.array([6, -3, -2])
x = np.array([8.5, -11.25, 0.25])
class Test(unittest.TestCase):



#    def test_linalg(self):
#        np.testing.assert_array_equal(solvers.linalg_solve(A, b), x)
#
#
#    def test_iterative(self):
#        np.testing.assert_array_almost_equal(solvers.iterative(A, b), x, 7)

    def test_huge(self):
        n = 3
        m = 5
        Ar = np.array([0])
        while np.any(np.diag(Ar) == 0):
            Ar = np.random.randint(-m, m, (n, n)).astype(np.float32)
        xr = np.random.randint(-m, m, (n)).astype(np.float32)
        br = np.dot(Ar, xr)
        print Ar
        print xr
        print br
        print solvers.linalg_solve(Ar, br)
        print solvers.iterative(Ar, br, xr + 1, 5, 10)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_linalg']
    unittest.main()
