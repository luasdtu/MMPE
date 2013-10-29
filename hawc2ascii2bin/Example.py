'''
Created on 06/09/2013

@author: Mads M. Pedersen (mmpe@dtu.dk)
'''
from __future__ import division, print_function, absolute_import, \
    unicode_literals
from hawc2ascii2bin import ascii2bin
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass

ascii2bin(r"unit_test/hawc2ascii.sel", "temp_hawc2ascii.sel")

