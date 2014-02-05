'''
Created on 21/01/2013

@author: Mads
'''
import glob
import matplotlib
import os
import shutil
import sys
import time
import zipfile
NUMPY = 'numpy'
MATPLOTLIB = 'matplotlib'
GUIDATA = 'guidata'
PYQT4 = 'PyQt4'
PYSIDE = 'PySide'
SCIPY = 'scipy'
CTYPES = '_ctypes'
MULTIPROCESSING = '_multiprocessing'

def build_exe(filename, version="1.0.0", description="", author="", modules=[NUMPY], includes=[], packages="[]", include_files=[], icon=None):
    basename = filename.replace('.py', '')
    folder = '%s_dist/' % basename
    prepare(modules)
    write_setup(basename, version, description, author, modules, includes, packages, include_files, icon)

    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.system('%s setup.py build' % sys.executable)
    shutil.move('./build/', folder)
    os.remove('setup.py')
    clean(modules)

    print "distribution created (%s/)" % ("../%s_dist" % basename)

def build_msi(filename, version, description="", author=""):
    basename = filename.replace('.py', '')
    folder = '%s_dist/' % basename
    if os.path.exists(folder):
        shutil.rmtree(folder)
    write_setup(basename, version, description, author)
    os.system('python setup.py bdist_msi')

    shutil.move('./dist/', '%s/' % folder)

    os.remove('setup.py')
    shutil.rmtree('build')
    shutil.rmtree('dist')

    print "Installer created (%s/)" % (folder)


def write_setup(name, version, description="", author="", modules=[NUMPY], includes=[], packages="[]", include_files=[], icon=None):
    """['appfuncs','gui_test']"""
    """["graphics/", "imageformats/", ]"""
    """"includes":["sip"],"""
    imports = []
    base = ""
    excludes = ['PyQt4.uic.port_v3', 'Tkconstants', 'tcl', 'tk', 'doctest', '_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'Tkinter',
                'tables', 'zmq', 'win32', 'Pythonwin', 'PySide', 'Cython', 'statmodels', 'cvxopt', 'PIL', '_sqlite3', '_ssl', '_testcapi',
                'markupsafe', 'numexpr', '_elementtree', '_hashlib', '_testcapi', 'bz2', 'simplejson', 'pyexpat',
                MATPLOTLIB, GUIDATA, PYQT4, PYSIDE, SCIPY, NUMPY, MULTIPROCESSING, CTYPES]
    #'pandas', '_socket', 'sip',
    if MATPLOTLIB in modules:
        include_files.append("""( matplotlib.get_data_path(),"mpl-data")""")
        imports.append("import matplotlib")

    if GUIDATA in modules:
        include_files.append("'guidata/images/'")
    if PYQT4 in modules:
        include_files.append("'imageformats/'")
        includes.append("'sip'")
        base = "base='Win32GUI', "
    if SCIPY in modules:
        imports.append("import scipy.sparse.csgraph")
        includes.append("""'scipy.sparse.csgraph._validation', 'scipy.sparse.linalg.dsolve.umfpack',
        'scipy.integrate.vode', 'scipy.integrate._ode','scipy.integrate.lsoda'""")

    for m in modules:
        excludes.remove(m)



    imports = "\n".join(imports)
    include_files = "[" + ",".join(include_files) + "]"
    includes = "[" + ",".join(includes) + "]"

    if icon is not None:
        icon = "icon='%s', " % icon
    else:
        icon = ""

    with open('setup.py', 'w') as fid:
        fid.writelines("""from cx_Freeze import setup, Executable
%s

build_exe_options = {
"includes": %s,
"packages": %s,
'excludes' : %s,

"include_files": %s}

setup(
name = "%s",
version="%s",
description="%s",
author = "%s",
options = { "build_exe": build_exe_options},
executables = [Executable("%s.py", %s%sshortcutName="%s", shortcutDir="DesktopFolder")])
    """ % (imports, includes, packages, excludes, include_files, name, version, description, author, name, base, icon, name))


def prepare(modules):
    if GUIDATA in modules:
        if not os.path.isdir("guidata"):
            os.mkdir("guidata/")
        if not os.path.isdir("guidata/images/"):
            shutil.copytree(r"%s/Lib/site-packages/guidata/images/" % os.path.dirname(sys.executable), "guidata/images/")
    if PYQT4 in modules:
        copy_imageformats()


def clean(modules):
    if GUIDATA in modules:
        if os.path.isdir("guidata"):
            shutil.rmtree("guidata/")
    if PYQT4 in modules:
        if os.path.isdir('imageformats'):
            shutil.rmtree('imageformats/')

def copy_imageformats():
    """
    Run this function if icons are not loaded
    """
    from PyQt4 import QtCore
    import sys
    app = QtCore.QCoreApplication(sys.argv)
    qt_library_path = QtCore.QCoreApplication.libraryPaths()


    imageformats_path = None
    for path in qt_library_path:
        if os.path.exists(os.path.join(str(path), 'imageformats')):
            imageformats_path = os.path.join(str(path), 'imageformats')
            local_imageformats_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imageformats')
            local_imageformats_path = os.path.join(os.getcwd(), 'imageformats')
            if not os.path.exists(local_imageformats_path):
                os.mkdir(local_imageformats_path)
            for file in glob.glob(os.path.join(imageformats_path, '*')):
                shutil.copy(file, os.path.join(local_imageformats_path, os.path.basename(file)))

