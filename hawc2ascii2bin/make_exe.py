'''
Created on 06/09/2013

@author: Mads M. Pedersen (mmpe@dtu.dk)
'''
from __future__ import division, print_function, absolute_import, unicode_literals
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass

import build_cx_exe
build_cx_exe.build_exe("hawc2ascii2bin.py", version="1.0.1")
