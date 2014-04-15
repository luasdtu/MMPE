'''
Created on 21/01/2013

@author: Mads
'''
from __future__ import division, absolute_import, unicode_literals
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass
import numpy as np
import glob
import os
import shutil
import sys
import time
import zipfile
from functions.io import make_dirs
from functions.io.make_dirs import make_packages
NUMPY = 'numpy'
MATPLOTLIB = 'matplotlib'
GUIDATA = 'guidata'
PYQT4 = 'PyQt4'
PYSIDE = 'PySide'
SCIPY = 'scipy'
CTYPES = '_ctypes'
MULTIPROCESSING = '_multiprocessing'
DOCX = "docx"
OPENGL = "_opengl"
PIL = "PIL"
HDF5 = "h5py"
PANDAS = 'pandas'

def build_exe(filename, version="1.0.0", description="", author="", modules=[NUMPY], includes=[], packages="[]", include_files=[], icon=None):
    basename = filename.replace('.py', '')
    folder = '%s_dist/' % basename
    prepare(modules)
    #write_setup(filename)

    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.system('%s setup.py py2exe' % sys.executable)
    #shutil.move('./build/', folder)
    #os.remove('setup.py')
    #clean(modules)

    print ("distribution created (%s/)" % folder)




def write_setup(filename):
    with open('setup.py', 'w') as fid:
        fid.writelines("""from distutils.core import setup
import py2exe

setup(console=['%s'])
    """ % (filename))


def prepare(modules):
    clean(modules)
    if GUIDATA in modules:
        if not os.path.isdir("guidata"):
            os.mkdir("guidata/")
        if not os.path.isdir("guidata/images/"):
            shutil.copytree(r"%s/Lib/site-packages/guidata/images/" % os.path.dirname(sys.executable), "guidata/images/")
    if PYQT4 in modules:
        copy_imageformats()
    if DOCX in modules:
        from functions.docx_document import docx_document
        source_path = os.path.dirname(docx_document.__file__)
        dest_path = "functions/docx_document/"
        make_dirs(dest_path)
        for folder in ['docx-template_clean', 'inkscape']:
            shutil.copytree(os.path.join(source_path, folder), os.path.join(dest_path, folder))



def clean(modules):
    if GUIDATA in modules:
        if os.path.isdir("guidata"):
            shutil.rmtree("guidata/")
    if PYQT4 in modules:
        if os.path.isdir('imageformats'):
            shutil.rmtree('imageformats/')
    if DOCX in modules:
        if os.path.isdir('functions'):
            shutil.rmtree('functions')
    if SCIPY in modules:
        from scipy.sparse.sparsetools import csr, csc, coo, dia, bsr, csgraph
        for f in [csr._csr.__file__,
                  csc._csc.__file__,
                  coo._coo.__file__,
                  dia._dia.__file__,
                  bsr._bsr.__file__,
                  csgraph._csgraph.__file__]:
            if os.path.isfile(os.path.basename(f)):
                os.remove(os.path.basename(f))
    if HDF5 in modules:
        #from h5py import _conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils
        #for f in [_conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils]:
        #    f = f.__file__
        #    shutil.copy(f, "h5py." + os.path.basename(f))
        #    include_files.append("'h5py.%s'" % os.path.basename(f))
        shutil.rmtree("h5py/", ignore_errors=True)



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

