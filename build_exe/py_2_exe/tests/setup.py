from distutils.core import setup
import py2exe
import matplotlib
import sys
import zmq
import os
os.environ["PATH"] = os.environ["PATH"] + os.path.pathsep + os.path.split(zmq.__file__)[0]



opts = {"py2exe":{"bundle_files"}}
sys.argv.append('py2exe')
opts = {'py2exe':
        {"bundle_files" : 3,
         "includes" : [ "matplotlib.backends", "matplotlib.backends.backend_qt4agg", "pylab", "numpy", "matplotlib.backends.backend_tkagg",
                       "zmq.utils", "zmq.utils.jsonapi", "zmq.utils.strtypes"],
         'excludes':['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg', '_fltkagg', '_gtk', '_gtkcairo'],
         'dll_excludes': ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll']}}
setup(console=['my_program.py'], zipfile=None, options=opts, data_files=matplotlib.get_py2exe_datafiles())
