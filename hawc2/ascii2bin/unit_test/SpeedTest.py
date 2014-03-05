'''
Created on 29/10/2013

@author: mmpe
'''

import os
import sys
import time
import unittest

from hawc2ascii2bin import cy_hawc2ascii2bin
from hawc2ascii2bin.hawc2ascii2bin import ascii2bin


class Test(unittest.TestCase):

    def setUp(self):
        sys.path.append("../")
        self.fn = r"C:\tmp\oc4_p2_load_case_1-3a"

    def test_pandas_Ascii2bin(self):
        fn = self.fn
        for f in [fn + "_bin.sel", fn + "_bin.dat"]:
            if os.path.exists(f):
                os.remove(f)
        t = time.time()
        ascii2bin(fn + ".sel")
        print time.time() - t

    def test_cy_Ascii2bin(self):
        fn = self.fn
        for f in [fn + "_bin.sel", fn + "_bin.dat"]:
            if os.path.exists(f):
                os.remove(f)
        t = time.time()
        cy_hawc2ascii2bin.ascii2bin(fn + ".sel")
        print time.time() - t

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
