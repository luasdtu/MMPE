import os
from MyQt.Qsci_replacement.LineTextWidget import LineTextWidget
d = None
d = dir()

gui = os.environ.get('QT_API', "pyqt")
if gui == "pyqt":
    from PyQt4.Qsci import *
elif gui == "pyside":
    QsciScintilla = LineTextWidget
    pass
else:
    pass


__all__ = [m for m in set(dir()) - set(d)]

