'''
Created on 15/01/2014

@author: MMPE
'''
import unittest

from functions.geometric import rad, deg
from functions.geometric.euler import *
import numpy as np


class Test(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.npEqual = np.testing.assert_array_equal
        self.npAlmostEqual = np.testing.assert_array_almost_equal

    def test_xyz2euler(self):
        np.testing.assert_array_almost_equal(xyz2euler(0, 0, 0), np.array([1, 0, 0, 0]))
        e0 = np.cos(rad(45) / 2)
        np.testing.assert_array_almost_equal(xyz2euler(rad(45), 0, 0), np.array([e0, 0, 0, np.sqrt(1 - e0 ** 2)]))

    def test_euler2angle(self):
        self.assertAlmostEqual(euler2angle(xyz2euler(rad(45), 0, 0)), rad(45))


    def test_euler2A(self):
        x, y, z = rad(30) , 0, 0
        e = xyz2euler(rad(30) , 0, 0)
        s = np.sin(rad(30))
        c = np.cos(rad(30))
        self.npAlmostEqual(euler2A(e), np.array([[c, -s, 0],
                                                 [s, c, 0],
                                                 [0, 0, 1]]))

    def test_A2xyz(self):
        s = np.sin(rad(30))
        c = np.cos(rad(30))
        self.npEqual(np.array([0, 0, 30]), deg(A2xyz(np.array([[c, -s, 0],
                                                               [s, c, 0],
                                                               [0, 0, 1]]))))

    def test_A2euler(self):
        e = xyz2euler(rad(30), 0, 0)
        A = euler2A(e)
        self.npEqual(e, A2euler(A))


    def test_euler2gl(self):
        self.npAlmostEqual(euler2gl(xyz2euler(rad(30), 0, 0)), np.array([ 30., 0. , 0.   , 0.25881905]))

    def test(self):
        print xyz2euler(0, rad(60), 0)
        e = xyz2euler(0, rad(60), 0)
        A = euler2A(e)
        print A2euler(A)

        print np.round(euler2A([ 0.8660254 , 0.   , -0.5      , 0.       ]), 4)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
