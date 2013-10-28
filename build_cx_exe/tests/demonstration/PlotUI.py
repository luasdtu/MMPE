# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../build_cx_exe\tests\demonstration\PlotUI.ui'
#
# Created: Wed Oct 23 15:00:21 2013
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mplcontainer = QtGui.QGridLayout()
        self.mplcontainer.setObjectName("mplcontainer")
        self.horizontalLayout.addLayout(self.mplcontainer)
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.actionUpdate = QtGui.QAction(Form)
        self.actionUpdate.setObjectName("actionUpdate")

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("editingFinished()"), self.actionUpdate.trigger)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpdate.setText(QtGui.QApplication.translate("Form", "update", None, QtGui.QApplication.UnicodeUTF8))

