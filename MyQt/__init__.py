class NoneQt(object):
    def __init__(self, *args, **kwargs):
        pass

QtCore = None
QtGui = None
QSci = None
ui_compiler = None

import sys
import os
gui = os.environ.get('QT_API', "pyqt")

if gui == "pyqt":
    try:
        QtCore = __import__("PyQt4.QtCore").QtCore
        QtGui = __import__("PyQt4.QtGui").QtGui
        try:
            Qsci = __import__("PyQt4.Qsci").Qsci
        except:
            pass
        ui_compiler = "pyuic4"
    except:
        gui = "pyside"
if gui == "pyside":
    os.environ['QT_API'] = gui
    QtCore = __import__("PySide.QtCore").QtCore
    QtGui = __import__("PySide.QtGui").QtGui
    try:
        Qsci = __import__("Qsci", globals(), locals(), ['Qsci'])
    except:
        pass
    ui_compiler = "pyside-uic"

if gui == "none":
    QtCore = None
    QtGui = None

print "Using gui: " + gui


###elif gui==NONE:
#QtCore = __import__("PyQtText.QtCore").QtCore
#QtGui = __import__("PyQtText.QtGui").QtGui

