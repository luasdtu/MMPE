from PyQt4 import QtGui
import os
os.environ['QT_API'] = "pyqt"
from QtGuiLoader import QtMainWindowLoader
from build_cx_exe.tests.demonstration import PlotUI
from build_cx_exe.tests.demonstration.matplotlibwidget import MatplotlibWidget
from scipy.stats import stats
import numpy as np
class Plot(QtMainWindowLoader):
    def __init__(self):
        QtMainWindowLoader.__init__(self, PlotUI)
        self.mpl = MatplotlibWidget()
        self.ui.mplcontainer.addWidget(self.mpl)
        self.setWindowIcon(QtGui.QIcon('Pydap.ico'))

    def actionUpdate(self):
        x = np.arange(-np.pi, np.pi, np.pi / 10)
        if str(self.ui.lineEdit.text()) != "":
            y = eval(str(self.ui.lineEdit.text()));
            self.mpl.axes.plot(x, y, '--rx', linewidth=2);
            self.mpl.axes.set_title('Sine Function');
            self.mpl.draw()
            print stats.mode([1, 2, 3, 3, 4, 5])


Plot().start()
