import sys
from threading import Thread
import time

from MyQt import QtCore, QtGui
import threading
import inspect
import collections
try:
    from MyQt.QtCore import QString
except:
    QString = str


class CancelWarning(Warning):
    pass


class QtProgressInformation(object):
    def __init__(self, parent):
        self._parent = parent
        self._progressDialog = QtGui.QProgressDialog(self._parent)
        self._progressDialog.setMinimumWidth(300)
        self._progressDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self._progressDialog.setMinimumDuration(0)
        self.progress_iterator = lambda seq, text = "Working... Please wait", allow_cancel = True, self = self : self.QtProgressIterator(self, seq, text, allow_cancel)


    def __show(self, text, allow_cancel, max_value=0):
        if not hasattr(self, '_progressDialog'):
            raise Exception ("%s inheriting QtProgressInformation must call QtProgressInformation.__init__" % self.__class__.__name__)
        self._progressDialog.reset()  #reset cancel flag
        self._progressDialog.setWindowTitle(text)
        self._progressDialog.setMaximum(max_value)

        cancel_text = (QString(), "Cancel")[allow_cancel]
        self._progressDialog.setCancelButtonText(cancel_text)
        self._progressDialog
        self._progressDialog.show()
        QtGui.QApplication.processEvents()

    def __hide(self):
        self._progressDialog.hide()
        self._progressDialog.close()
        QtGui.QApplication.processEvents()

    class QtProgressIterator(collections.Iterator):
        def __init__(self, QtProgressInformation, seq, text, allow_cancel=True):
            self.QtProgressInformation = QtProgressInformation
            self.generator = iter(seq)

            self.allow_cancel = allow_cancel
            self.n = 0
            self.QtProgressInformation._QtProgressInformation__show(text, allow_cancel, self.generator.__length_hint__())


        def __del__(self):
                self.QtProgressInformation._QtProgressInformation__hide()
                pass

        def __iter__(self):
                return self

        def next(self):
            # required by python 2
            return self.__next__()

        def __next__(self):
            if self.allow_cancel and self.QtProgressInformation._progressDialog.wasCanceled():
                raise CancelWarning()
            self.QtProgressInformation._progressDialog.setValue(self.n)
            self.n += 1
            try:
                return self.generator.__next__()
            except AttributeError:
                return self.generator.next()  #in python 2, iterators __next__ is named next


#    def progress_iterator(self, sequence, text="Working... Please wait", allow_cancel=True):
#        it = iter(sequence)
#        if it.__length_hint__() > 0:
#            self.__show(text, allow_cancel, it.__length_hint__())
#            for n, v in enumerate(it):
#                if allow_cancel and self._progressDialog.wasCanceled():
#                    raise CancelWarning()
#                self._progressDialog.setValue(n)
#                yield(v)
#            self._progressDialog.hide()
#            QtGui.QApplication.processEvents()

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
            return QtProgressInformation(parent).exec_long_task(text, allow_cancel, task, *args, **kwargs)
        return taskWrapper
    return wrap


#
if __name__ == "__main__":
    class MW(QtGui.QMainWindow, QtProgressInformation):
        def __init__(self):
            QtGui.QMainWindow.__init__(self)
            QtProgressInformation.__init__(self, self)


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

#            print (task1a(1))
#
#            try:
#                print (task1b(3))
#            except CancelWarning:
#                print ("task1b cancelled")
#
#
#            print (self.exec_long_task("exec_long_task(without cancel)", False, task2a, 1))
#
#            try:
#                print (self.exec_long_task("exec_long_task(with cancel", True, task2b, 5))
#            except CancelWarning:
#                print ("task2 cancelled")

            try:
                for x in self.progress_iterator(xrange(100), "progressbar(without cancel)", False):
                    t = time.clock()
                    while time.clock() - t < .01:
                        pass
                    if x > 80:
                        raise Exception
            except Exception as e:
                print (str(e))

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

