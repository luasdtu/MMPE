'''
Created on 11/07/2013

@author: mmpe
'''

import build_cx_exe
import inspect
import os
import shutil
import subprocess
import unittest



class Test_exe(unittest.TestCase):




    def test_exe(self):
        if os.path.isdir("my_program_dist"):
            shutil.rmtree("my_program_dist/")
        build_cx_exe.build_exe('my_program.py', "2.0.0")
        self.assertTrue(os.path.isfile("my_program_dist/exe.win32-2.7/my_program.exe"))


    def test_pyqt4(self):
        if os.path.isdir("demonstration/pyqt_window_dist"):
            shutil.rmtree("demonstration/pyqt_window_dist/")
        build_cx_exe.build_exe('demonstration/pyqt_window.py', "2.0.0", modules=[build_cx_exe.PYQT4, build_cx_exe.SCIPY], icon='demonstration/pydap.ico')
        self.assertTrue(os.path.isfile("demonstration/pyqt_window_dist/exe.win32-2.7/pyqt_window.exe"))
        os.system("demonstration\\pyqt_window_dist\\exe.win32-2.7\\pyqt_window.exe")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
