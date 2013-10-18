import os
d = None
d = dir()


if os.environ.get('QT_API', "PyQt4") == "pyqt":
    from PyQt4.QtCore import *
else:
    from PySide.QtCore import *
    pyqtSignal = Signal
    QString = str


__all__ = [m for m in set(dir()) - set(d)]

