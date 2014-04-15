'''
Created on 18/03/2014

@author: mmpe
'''
import unittest
import os
import shutil
from build_exe.py_2_exe import build_p2exe


class Test(unittest.TestCase):


#    def test_hello_exe(self):
#        if os.path.isdir("hello_dist"):
#            shutil.rmtree("hello_dist/")
#        import pandas
#
#        build_p2exe.build_exe('hello.py')
#        self.assertTrue(os.path.isfile("my_program_dist/exe.win32-2.7/my_program.exe"))

    def test_myprogram_exe(self):
        if os.path.isdir("dist"):
            shutil.rmtree("dist")


        build_p2exe.build_exe('my_program.py')
        #self.assertTrue(os.path.isfile("my_program_dist/exe.win32-2.7/my_program.exe"))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
