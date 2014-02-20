
import os
from MyQt import QtGui, QtCore
from MyQt.QtGui import QMessageBox, QFileDialog
from ui.qt_progress_information import QtProgressInformation


class QtOutputUI(object):
    def show_message(self, msg, title="Information"):
        QMessageBox.information(self, title, msg)

    def show_warning(self, msg, title="Warning"):
        QMessageBox.warning(self, title, msg)

    def show_error(self, msg, title="Error"):
        QMessageBox.critical(self, title, msg)

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
        if fn == "": cencel
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

    def get_folder_name(self, title='Select directory', file_dir=None):
        file_dir = self._default_dir(file_dir)
        r = str(QFileDialog.getExistingDirectory(self, title)).replace('\\', '/')
        if len(r) > 0:
            self.save_setting("default_dir", os.path.dirname(r[0]))
        return r





class QtStatusUI(QtProgressInformation):
    def __init__(self, parent):
        QtProgressInformation.__init__(self, parent)

    def start_wait(self):
        """Changes mouse icon to waitcursor"""
        QtCore.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    def end_wait(self):
        """Restores default mouse icon"""
        QtCore.QApplication.restoreOverrideCursor()


class QtUI(QtOutputUI, QtInputUI, QtStatusUI):
    def __init__(self, parent):
        QtStatusUI.__init__(self, parent)
