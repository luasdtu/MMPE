import os
from MyQt.Qsci_replacement.LineTextWidget import LineTextWidget
d = None
d = dir()


if os.environ.get('QT_API', "pyqt") == "pyqt":
    from PyQt4.Qsci import *
else:
    QsciScintilla = LineTextWidget
    pass


__all__ = [m for m in set(dir()) - set(d)]

