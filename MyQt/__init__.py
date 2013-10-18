

QtCore = None
QtGui = None
QSci = None
ui_compiler = None

import sys
import os
gui = os.environ.get('QT_API', "pyqt")
if gui == "pyqt":
    QtCore = __import__("PyQt4.QtCore").QtCore
    QtGui = __import__("PyQt4.QtGui").QtGui
    ui_compiler = "pyuic4"
elif gui == "pyside":
    QtCore = __import__("PySide.QtCore").QtCore
    QtGui = __import__("PySide.QtGui").QtGui
    Qsci = __import__("Qsci", globals(),locals(), ['Qsci'])
    ui_compiler = "pyside-uic"
elif gui == "none":
    QtCore = None
    QtGui = None
else:
    raise NotImplementedError
    
###elif gui==NONE:
#QtCore = __import__("PyQtText.QtCore").QtCore
#QtGui = __import__("PyQtText.QtGui").QtGui

