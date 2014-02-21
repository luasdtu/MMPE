'''
Created on 15/01/2014

@author: MMPE
'''
import unittest

from functions.geometric import rad, deg
from functions.geometric.euler import *
import numpy as np

npEqual = np.testing.assert_array_equal
npAlmostEqual = np.testing.assert_array_almost_equal
class Test(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)




    def test_euler2angle(self):
        e0 = np.cos(rad(30) / 2)
        self.assertAlmostEqual(euler2angle(np.array([e0, np.sqrt(1 - e0 ** 2), 0, 0])), rad(30))


    def test_euler2A(self):
        e0 = np.cos(rad(30) / 2)
        e1 = np.sqrt(1 - e0 ** 2)
        npAlmostEqual(euler2A(np.array([e0, e1, 0, 0])), Ax(rad(30)))
        npAlmostEqual(euler2A(np.array([e0, 0, e1, 0])), Ay(rad(30)))
        npAlmostEqual(euler2A(np.array([e0, 0, 0, e1])), Az(rad(30)))

    def test_A2euler(self):
        e0 = np.cos(rad(30) / 2)
        e1 = np.sqrt(1 - e0 ** 2)
        npAlmostEqual(A2euler(Ax(rad(30))), np.array([e0, e1, 0, 0]))
        npAlmostEqual(A2euler(Ay(rad(30))), np.array([e0, 0, e1, 0]))
        npAlmostEqual(A2euler(Az(rad(30))), np.array([e0, 0, 0, e1]))


#    def test_xyz2A(self):
#        print deg(A2xyz(xyz2A(rad(10), rad(12.5), rad(14.5))))



    #    def test_A2euler(self):
#        e = xyz2euler(rad(30), 0, 0)
#        A = euler2A(e)
#        self.npEqual(e, A2euler(A))


#
#    def test_A2xyz(self):
#        s = np.sin(rad(30))
#        c = np.cos(rad(30))
#        self.npEqual(np.array([30, 0, 0]), deg(A2xyz(np.array([[1, 0, 0],
#                                                               [0, c, -s],
#                                                               [0, s, c]]))))
#        self.npEqual(np.array([0, 30, 0]), deg(A2xyz(np.array([[c, 0, s],
#                                                               [0, 1, 0],
#                                                               [-s, 0, c]]))))
#        self.npEqual(np.array([0, 0, 30]), deg(A2xyz(np.array([[c, -s, 0],
#                                                               [s, c, 0],
#                                                               [0, 0, 1]]))))
#
#        A = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
#        #self.npEqual(A, xyz2A(*A2xyz(A)))

#
#    def test_xyz2euler(self):
#        np.testing.assert_array_almost_equal(xyz2euler(0, 0, 0), np.array([1, 0, 0, 0]))
#        e0 = np.cos(rad(30) / 2)
#        np.testing.assert_array_almost_equal(xyz2euler(rad(30), 0, 0), np.array([e0, np.sqrt(1 - e0 ** 2), 0, 0]))
#        np.testing.assert_array_almost_equal(xyz2euler(0, rad(30), 0), np.array([e0, 0, np.sqrt(1 - e0 ** 2), 0]))
#        np.testing.assert_array_almost_equal(xyz2euler(0, 0, rad(30)), np.array([e0, 0, 0, np.sqrt(1 - e0 ** 2)]))


#    def test_A2euler(self):
#        e = xyz2euler(rad(30), 0, 0)
#        A = euler2A(e)
#        self.npEqual(e, A2euler(A))
#
#
#    def test_euler2gl(self):
#        self.npAlmostEqual(euler2gl(xyz2euler(rad(30), 0, 0)), np.array([ 30., 0. , 0.   , 0.25881905]))
#
##    def test(self):
##        print xyz2euler(0, rad(60), 0)
##        e = xyz2euler(0, rad(60), 0)
##        A = euler2A(e)
##        print A2euler(A)
##
##        print np.round(euler2A([ 0.8660254 , 0.   , -0.5      , 0.       ]), 4)
#


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
