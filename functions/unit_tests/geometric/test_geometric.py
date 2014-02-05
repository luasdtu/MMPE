'''
Created on 15/01/2014

@author: MMPE
'''
import unittest

from functions.geometric import rad, deg
import numpy as np


class Test(unittest.TestCase):


    def test_rad(self):
        self.assertEqual(rad(45), np.pi / 4)
        self.assertEqual(rad(135), np.pi * 3 / 4)


    def test_deg(self):
        self.assertEqual(45, deg(np.pi / 4))
        self.assertEqual(135, deg(np.pi * 3 / 4))

    def test_rad_deg(self):
        for i in [15, 0.5, 355, 400]:
            self.assertEqual(i, deg(rad(i)), i)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_rad']
    unittest.main()
