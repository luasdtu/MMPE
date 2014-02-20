from __future__ import division, absolute_import, unicode_literals
import os
d = None;d = dir()


from .makedirs import makedirs

def read_file(path, default=None):
    if os.path.isfile(path):
        with open(path) as fid:
            return fid.read()
    else:
        return default

__all__ = [m for m in set(dir()) - set(d)]