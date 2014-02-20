'''
Created on 06/02/2014

@author: MMPE
'''

from __future__ import division, absolute_import, unicode_literals
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass
import os
import errno

def makedirs(path):
    path = os.path.realpath(os.path.dirname(path))
    folders = path.split(os.path.sep)

    for i in range(len(folders)):
        folder = os.path.sep.join(folders[:i + 1])
        try:
            os.mkdir(folder)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

