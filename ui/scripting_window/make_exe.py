'''
Created on 06/09/2013

@author: Mads M. Pedersen (mmpe@dtu.dk)
'''
from __future__ import division, print_function, absolute_import, unicode_literals
from build_exe.cx.build_cx_exe import NUMPY, PYQT4, MULTIPROCESSING
import os
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass

from build_exe.cx import build_cx_exe
build_cx_exe.build_exe("controller.py", version="1.0.0", modules=[PYQT4, MULTIPROCESSING, NUMPY],
                       includes=["PyQt4.QtNetwork", "MyQt.Qsci"],
                       include_files=['docs/doc.html', 'docs/source.html', 'docs/index.html', 'docs/ScriptFunctions.html', 'docs/_static/', 'docs/_modules'],
                       packages=['appfuncs'])
os.system('controller_dist\\exe.win32-2.7\\controller.exe')