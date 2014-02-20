import sys
from threading import Thread
import time

from MyQt import QtCore, QtGui
import threading
import inspect


class CancelWarning(Warning):
    pass


class QtProgressInformation(object):
    def __init__(self, parent):
        self._parent = parent
        self._progressDialog = QtGui.QProgressDialog(self._parent)
        self._progressDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self._progressDialog.setMinimumDuration(0)


    def __show(self, text, allow_cancel, max_value=0):
        self._progressDialog.reset()  #reset cancel flag
        self._progressDialog.setWindowTitle(text)
        self._progressDialog.setMaximum(max_value)
        cancel_text = ("", "Cancel")[allow_cancel]
        self._progressDialog.setCancelButtonText(cancel_text)
        self._progressDialog.show()

    def __hide(self):
        self._progressDialog.hide()

    def progress_iterator(self, sequence, text="Working... Please wait", allow_cancel=True):
        it = iter(sequence)
        if it.__length_hint__() > 0:
            self.__show(text, allow_cancel, it.__length_hint__())
            for n, v in enumerate(it):
                if allow_cancel and self._progressDialog.wasCanceled():
                    raise CancelWarning()
                self._progressDialog.setValue(n)
                yield(v)
            self._progressDialog.hide()

    def exec_long_task(self, text, allow_cancel, task, *args, **kwargs):
        class TaskThread(Thread):
            result = None
            def __init__(self, task, *args, **kwargs):
                Thread.__init__(self)
                self.task = lambda: task(*args, **kwargs)

            def run(self):
                self.result = self.task()

        class CancelableTaskThread(TaskThread):
            def __init__(self, task, *args, **kwargs):
                self.cancel_event = threading.Event()
                if "cancel_event" not in inspect.getargspec(task)[0]:
                    raise TypeError("Cancelable tasks must take a 'cancel_event'-argument")
                kwargs['cancel_event'] = self.cancel_event
                TaskThread.__init__(self, task, *args, **kwargs)

#        class TaskQThread(QtCore.QThread):
#            result = None
#            def __init__(self, _parent, task, *args, **kwargs):
#                QtCore.QThread.__init__(self)
#                self.task = lambda: task(*args, **kwargs)
#
#            def run(self):
#                self.result = self.task()
#        t = TaskQThread(self, task, *args, **kwargs)
#        t.start()
#        while t.isRunning():
#            time.sleep(0.1)
#            QtGui.QApplication.processEvents()


        self.__show(text, allow_cancel)
        if allow_cancel:
            t = CancelableTaskThread(task, *args, **kwargs)
        else:
            t = TaskThread(task, *args, **kwargs)

        t.start()
        while t.is_alive():
            time.sleep(0.1)
            if allow_cancel and self._progressDialog.wasCanceled():
                t.cancel_event.set()
                t.join()
                raise CancelWarning
            QtGui.QApplication.processEvents()
        t.join()
        self.__hide()



        return t.result


def long_task(parent=None, text="Working", allow_cancel=False):
    def wrap(task):
        def taskWrapper(*args, **kwargs):
            return ProgressInformation(_parent).exec_long_task(text, allow_cancel, task, *args, **kwargs)
        return taskWrapper
    return wrap


#
if __name__ == "__main__":

    class MW(QtGui.QMainWindow, ProgressInformation):
        def __init__(self):
            QtGui.QMainWindow.__init__(self)
            ProgressInformation.__init__(self, self)


        def mouseDoubleClickEvent(self, *args, **kwargs):

            @long_task(self, "decorator(without cancel)", False)
            def task1a(sec):
                t = time.clock()
                while time.clock() - t < sec:
                    pass
                return "result of task1a"

            @long_task(self, "decorator(with cancel)", True)
            def task1b(sec, cancel_event):
                t = time.clock()
                while time.clock() - t < sec:
                    if cancel_event.isSet():
                        break
                return "result of task1b"

            def task2a(sec):
                t = time.clock()
                while time.clock() - t < sec:
                    pass
                return "result of task2a"

            def task2b(sec, cancel_event):
                t = time.clock()
                while time.clock() - t < sec:
                    if cancel_event.isSet():
                        break
                return "result of task2b"

            print (task1a(1))

            try:
                print (task1b(3))
            except CancelWarning:
                print ("task1b cancelled")


            print (self.exec_long_task("exec_long_task(without cancel)", False, task2a, 1))

            try:
                print (self.exec_long_task("exec_long_task(with cancel", True, task2b, 5))
            except CancelWarning:
                print ("task2 cancelled")



            for _ in self.progress_iterator(xrange(100), "progressbar(without cancel)", False):
                t = time.clock()
                while time.clock() - t < .01:
                    pass

            try:
                for _ in self.progress_iterator(xrange(100), "progressbar(with cancel)", True):
                    t = time.clock()
                    while time.clock() - t < .05:
                        pass
            except CancelWarning:
                print ("progressbar cancelled")
            return QtGui.QMainWindow.mouseDoubleClickEvent(self, *args, **kwargs)


    app = QtGui.QApplication(sys.argv)
    mw = MW()
    mw.show()
    sys.exit(app.exec_())

