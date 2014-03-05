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

def make_dirs(path):
    path = os.path.realpath(os.path.dirname(path))
    folders = path.split(os.path.sep)

    for i in range(len(folders)):
        folder = os.path.sep.join(folders[:i + 1])
        try:
            os.mkdir(folder)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

def make_packages(path):
    path = os.path.realpath(os.path.dirname(path))
    folders = path.split(os.path.sep)

    for i in range(len(folders)):
        folder = os.path.sep.join(folders[:i + 1])
        try:
            os.mkdir(folder)
            with open(os.path.join(folder, "__init__.py"), 'w') as fid:
                pass
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
