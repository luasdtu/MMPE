
import os
from MyQt import QtGui, QtCore
from MyQt.QtGui import QMessageBox, QFileDialog
from ui.qt_progress_information import QtProgressInformation
import sys
import traceback


class QtOutputUI(object):
    show_traceback = False

    def __init__(self):
        sys.stderr = self.show_error

    def run(self, f, *args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Warning as e:
            self.show_warning(e)
        except Exception as e:
            self.show_error(e)
            raise

    def show_box(self, box_func):
        cursor = QtGui.QApplication.overrideCursor()
        QtGui.QApplication.restoreOverrideCursor()
        box_func()
        if cursor and isinstance(cursor, QtGui.QCursor) and cursor.shape() == QtCore.Qt.WaitCursor:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        QtGui.QApplication.processEvents()



    def show_message(self, msg, title="Information"):
        self.show_box(lambda : QMessageBox.information(self, title, msg))

    def show_warning(self, msg, title="Warning"):
        """Show a warning dialog box
        msg: Error message or Warning object
        """
        if isinstance(msg, Warning):
            title = msg.__class__.__name__
            msg = str(msg)

        self.show_box(lambda : QMessageBox.warning(self, title, msg))

    def show_error(self, msg, title="Error"):
        """Show a warning dialog box
        msg: Error message or Exception object
        """
        if isinstance(msg, Exception):
            e = msg
            title = e.__class__.__name__
            msg = str(e)
            if self.show_traceback:
                msg += "\n" + traceback.format_exc()
        self.show_box(lambda : QMessageBox.critical(self, title, msg))

    def show_text(self, text):
        raise NotImplementedError


class QtInputUI(object):

    def get_confirmation(self, title, msg):
        return QMessageBox.Yes == QMessageBox.question(self, title, msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def get_string(self, title, msg):
        return QMessageBox.question(self, title, msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    def get_open_filename(self, title="Open", filetype_filter="*.*", file_dir=None, selected_filter=None):
        """
        fn = gui.get_open_filename(title="Open", filetype_filter="*.dit1;*dit2;;*.dat", file_dir=".", selected_filter="*.dat")
        if fn == "": return #Cancel
        """
        if file_dir is None:
            file_dir = self._default_dir(file_dir)

        try:
            r = str(QFileDialog.getOpenFileName(self, title, file_dir, filetype_filter, selected_filter))
        except TypeError:
            r = str(QFileDialog.getOpenFileName(self, title, file_dir, filetype_filter))
        if isinstance(r, tuple):
            r = r[0]
        r = r.replace('\\', '/')
        if r != "":
            self.save_setting("default_dir", os.path.dirname(r))
        return r

    def get_save_filename(self, title, filetype_filter, file_dir=None, selected_filter=None):
        """
        fn = gui.get_save_filename(title="title", filetype_filter="*.dit1;*dit2;;*.dat", file_dir=".", selected_filter="*.dat")
        if fn == "": return #cancel
        """
        file_dir = self._default_dir(str(file_dir))
        r = str(QFileDialog.getSaveFileName(self, title, file_dir, filetype_filter, selected_filter))
        if isinstance(r, tuple):
            r = r[0]
        r = r.replace('\\', '/')
        if r != "":
            self.save_setting("default_dir", os.path.dirname(r))
        return r

    def _default_dir(self, file_dir):
        if file_dir is None or os.path.dirname(file_dir) == "":
            default_dir = self.load_setting('default_dir', '.')
            if os.path.isdir(default_dir):
                file_dir = default_dir
            else:
                file_dir = ""
        return file_dir

    def get_open_filenames(self, title, filetype_filter, file_dir=None):
        file_dir = self._default_dir(file_dir)
        r = QFileDialog.getOpenFileNames(self, title, file_dir, filetype_filter)
        if isinstance(r, tuple):
            r = r[0]
        r = [str(f).replace('\\', '/') for f in r]
        if len(r) > 0:
            self.save_setting("default_dir", os.path.dirname(r[0]))
        return r

    def get_foldername(self, title='Select folder', file_dir=None):
        file_dir = self._default_dir(file_dir)
        r = str(QFileDialog.getExistingDirectory(self, title, file_dir)).replace('\\', '/')
        if os.path.isdir(r):
            self.save_setting("default_dir", r)
        return r





class QtStatusUI(QtProgressInformation):

    def __init__(self, parent):
        QtProgressInformation.__init__(self, parent)

    def start_wait(self):
        """Changes mouse icon to waitcursor"""
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    def end_wait(self):
        """Restores default mouse icon"""
        QtGui.QApplication.restoreOverrideCursor()


class QtUI(QtOutputUI, QtInputUI, QtStatusUI):
    def __init__(self, parent):
        QtStatusUI.__init__(self, parent)
