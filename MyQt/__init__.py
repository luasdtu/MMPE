from functions import process_exec
class NoneQt(object):
    def __init__(self, *args, **kwargs):
        pass

QtCore = None
QtGui = None
QSci = None
ui_compiler = None
ui_compile_func = None
import sys
import os
gui = os.environ.get('QT_API', "pyqt")

if gui == "pyqt":
    try:
        QtCore = __import__("PyQt4.QtCore").QtCore
        QtGui = __import__("PyQt4.QtGui").QtGui
        QtWebKit = __import__("PyQt4.QtWebKit").QtWebKit
        Qsci = __import__("PyQt4.Qsci").Qsci

        ui_compiler = "pyuic4"
        uic = __import__('PyQt4.uic')

        def ui_compile_func(ui_file, py_file):
            pyuic_path = os.path.join(os.path.dirname(sys.executable), 'Lib/site-packages/PyQt4/uic/pyuic.py')
            os.system('"%s" %s %s > %s' % (sys.executable, pyuic_path, ui_file, py_file))
#            print os.getcwd()
#            process_exec.DEBUG = 1
#            errorcode, stdout, stderr = process_exec.pexec([sys.executable, pyuic_path, ('%s > %s' % (ui_file, py_file)).replace("\\", "/")], os.getcwd())
#            if errorcode:
#                print stdout
#                print stderr
#
        #ui_compile_func = lambda ui_file, py_file : uic.uic.compileUi(ui_file, open(py_file, 'w'))
    except:
        gui = "pyside"
if gui == "pyside":
    os.environ['QT_API'] = gui
    QtCore = __import__("PySide.QtCore").QtCore
    QtGui = __import__("PySide.QtGui").QtGui
    QtWebKit = __import__("PySide.QtWebKit").QtWebKit
    try:
        Qsci = __import__("Qsci", globals(), locals(), ['Qsci'])
    except:
        pass
    ui_compiler = "pyside-uic"
    ui_compile_func = lambda ui_file, py_file: os.system('"%s" %s > %s' % (ui_compiler, ui_file, py_file))


elif gui == "none":
    QtCore = None
    QtGui = None
    QtWebKit = None
    ui_compile_func = None
#print ("Using gui: " + gui)


###elif gui==NONE:
#QtCore = __import__("PyQtText.QtCore").QtCore
#QtGui = __import__("PyQtText.QtGui").QtGui

