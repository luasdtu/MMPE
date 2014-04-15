'''
Created on 11/07/2013

@author: mmpe
'''

from build_exe.cx import  build_cx_exe, PYQT4, SCIPY, MATPLOTLIB

import os
import shutil

import unittest
from build_exe.cx.build_cx_exe import NUMPY



class Test_exe(unittest.TestCase):




    def test_exe(self):
        if os.path.isdir("my_program_dist"):
            shutil.rmtree("my_program_dist/")
        import pandas

        build_cx_exe.build_exe('my_program.py', "2.0.0", modules=[NUMPY], includes=["'pandas'"])
        self.assertTrue(os.path.isfile("my_program_dist/exe.win32-2.7/my_program.exe"))



#    def test_pyqt4(self):
#        if os.path.isdir("demonstration/pyqt_window_dist"):
#            shutil.rmtree("demonstration/pyqt_window_dist/")
#        build_cx_exe.build_exe('demonstration/pyqt_window.py', "2.0.0", modules=[PYQT4, SCIPY, MATPLOTLIB, NUMPY], icon='demonstration/pydap.ico')
#        self.assertTrue(os.path.isfile("demonstration/pyqt_window_dist/exe.win32-2.7/pyqt_window.exe"))
#        os.system("demonstration\\pyqt_window_dist\\exe.win32-2.7\\pyqt_window.exe")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
