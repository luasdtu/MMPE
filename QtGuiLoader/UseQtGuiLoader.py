'''

Examples of how to use QtGuiLoader

@Created on 13/3/2013
@version: 1.5 (4/7-2013)
@author: Mads M Pedersen (mmpe@dtu.dk)
'''
from PyQt4 import QtGui, QtCore
from QtGuiLoader import QtMainWindowLoader, QtWidgetLoader, QtDialogLoader
import MyMainWindowUI
import MyWidgetUI

import sys


"""Use as MainWindow"""
class MyMainWindow(QtMainWindowLoader):
    def __init__(self, parent=None):
        QtMainWindowLoader.__init__(self, ui_module=MyWidgetUI)
        self.ui.lineEdit.setText("MyMainWindow")
        self.setWindowTitle("MyMainWindow")

    def actionPrintText(self):
        print "Mainwindow text: %s" % self.ui.lineEdit.text()
#run using
#MyMainWindow().start()


"""Use as Dialog (i.e. sub window, that closes with parent)"""
class MyDialog(QtDialogLoader):
    def __init__(self, parent, modal):
        QtDialogLoader.__init__(self, MyWidgetUI, parent, modal)
        self.ui.lineEdit.setText("MyDialog")
        self.setWindowTitle("MyDialog")

    def actionPrintText(self):
        print "Dialog text: %s" % self.ui.lineEdit.text()
##run using
#MyDialog(None,True,True).start()



"""Use as ui_widget with actionhandlers at parent(e.g. QMainWindow) subclass """
class WidgetWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtGui.QMainWindow.__init__(self, *args, **kwargs)
        self.widget = QtWidgetLoader(ui_module=MyWidgetUI, parent=self, action_receiver=self)
        self.widget.ui.lineEdit.setText("MyWidget")
        self.show()

    def actionPrintText(self):
        print "Widget text: %s" % self.widget.ui.lineEdit.text()


# #Run using:
# app = QtGui.QApplication(sys.argv)
# w = WidgetWindow()
# print w
# app.exec_()


"""Use as _ui_widget with actionhandlers in ui_widget subclass"""
class MyWidget(QtWidgetLoader):

    def __init__(self, parent):
        QtWidgetLoader.__init__(self, ui_module=MyWidgetUI, parent=parent)
        self.ui.lineEdit.setText("MyWidget")

    def actionPrintText(self):
        print "Widget text: %s" % self.ui.lineEdit.text()

# #run using
# app = QtGui.QApplication(sys.argv)
# window = QtGui.QMainWindow()
# w = MyWidget(window)
# print w
# window.show()
# app.exec_()


class MyMainWindowWithMenu(QtMainWindowLoader):
    def __init__(self):
        QtMainWindowLoader.__init__(self, MyMainWindowUI)

    def actionSayHello(self):
        print "hello"

#MyMainWindowWithMenu().start()



#-------------------------


class MyCombinationWindow(QtMainWindowLoader):
    def __init__(self):
        QtMainWindowLoader.__init__(self, ui_module=MyWidgetUI)
        self.setWindowTitle("Mainwindow")

        #Add as QWidget
        self.ui.horizontalLayout.addWidget(MyWidget(self))

        #Add button that opens as QDialog
        self.ui.horizontalLayout.addWidget(QtGui.QPushButton("Open dialog", self, clicked=self.open_dialog))

    def open_dialog(self):
        #open as QDialog
        MyDialog(parent=self, modal=True).start()

    def actionPrintText(self):
        print "Mainwindow text: %s" % self.ui.lineEdit.text()


def test(nr):
    if nr == 1:
        MyMainWindow().start()
    elif nr == 2:
        MyDialog(None, True).start()
    elif nr == 3:
        app = QtGui.QApplication(sys.argv)
        w = WidgetWindow()
        print w
        app.exec_()
    if nr == 4:
        app = QtGui.QApplication(sys.argv)
        window = QtGui.QMainWindow()
        w = MyWidget(window)
        print w
        window.show()
        app.exec_()
    if nr == 5:
        MyMainWindowWithMenu().start()
    if nr == 6:
        MyCombinationWindow().start()

for i in xrange(1, 7):
    test(i)
