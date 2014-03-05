'''
Created on 11/07/2013

@author: mmpe
'''




import os
import unittest

from functions.io import repeat_operation
from functions.io.repeat_operation import repeat



nr = 0
class Test_exe(unittest.TestCase):




    def test_repeat(self):

        p = 'temp.txt'
        f = open(p, 'w')

        def close(path):
            global nr
            nr += 1
            if nr > 2:
                f.close()
            else:
                os.remove(path)
        repeat(close, p)
        self.assertEqual(nr, 3)


    def test_repeat_no_succeed(self):
        repeat_operation.no_trials = 3
        p = 'temp.txt'
        f = open(p, 'w')

        self.assertRaises(WindowsError, repeat, os.remove, p)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
