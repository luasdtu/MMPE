import os
d = None
d = dir()

gui = os.environ.get('QT_API', "pyqt")
if gui == "pyqt":
    from PyQt4.QtWebKit import *
#elif gui == "pyside":
else:
    from PySide.QtWebKit import *
#else:
#    from MyQt import NoneQt
#    Qt = NoneQt
#    QThread = NoneQt
#    pyqtSignal = NoneQt


__all__ = [m for m in set(dir()) - set(d)]

