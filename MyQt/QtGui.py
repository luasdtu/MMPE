import os
d = None
d = dir()

if os.environ.get('QT_API', "pyqt") == "pyqt":
    from PyQt4.QtGui import *
else:
    from PySide.QtGui import *


__all__ = [m for m in set(dir()) - set(d)]

