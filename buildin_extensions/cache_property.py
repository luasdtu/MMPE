'''
Created on 07/02/2014

@author: MMPE
'''

from __future__ import division, absolute_import, unicode_literals
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass
import numpy as np


def set_cache_property(obj, name, get_func, set_func=None):
    _name = "_" + name
    setattr(obj, _name, None)
    def get(self):
        if getattr(obj, _name) is None:
            setattr(obj, _name, get_func())
        return getattr(obj, _name)

    p = property(lambda self:get(self), set_func)
    return setattr(obj.__class__, name, p)
