from __future__ import division, absolute_import, unicode_literals
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass
import numpy as np

def rad(deg):
    return deg * np.pi / 180

def deg(rad):
    return rad / np.pi * 180