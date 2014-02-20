'''
Created on 11/07/2013

@author: mmpe
'''

import inspect
import io_operations
import os
import unittest
from io_operations import makedirs
import shutil



nr = 0
class TestMakedir(unittest.TestCase):

    def test_makedir(self):
        path = "myfolder1/myfolder2/myfile.fil"
        shutil.rmtree('myfolder1', ignore_errors=True)
        makedirs(path)
        self.assertTrue(os.path.isdir("myfolder1/myfolder2/"))
        with open(path, 'w'):
            pass
        self.assertTrue(os.path.isfile(path))

        # repeat and check that file is not deleted
        makedirs("myfolder1/myfolder2/myfile.fil")
        self.assertTrue(os.path.isdir("myfolder1/myfolder2/"))
        self.assertTrue(os.path.isfile(path))




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
