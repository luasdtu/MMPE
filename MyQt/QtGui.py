
import os
d = None
d = dir()


gui = os.environ.get('QT_API', "pyqt")
if gui == "pyqt":
    from PyQt4.QtGui import *
else:
#elif gui == "pyside":
    from PySide.QtGui import *
#else:
#    from MyQt import NoneQt
#    QWidget = NoneQt()
#    QMainWindow = NoneQt()
#    QAction = NoneQt
#    QWidgetAction = NoneQt



__all__ = [m for m in set(dir()) - set(d)]

