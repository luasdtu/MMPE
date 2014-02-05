from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

ext_modules = [Extension("test_cython_compile_Cy_char", ["test_cython_compile_Cy_char.pyx"], include_dirs = [numpy.get_include()])]

setup(
name = 'name',
cmdclass = {'build_ext': build_ext},
ext_modules = ext_modules
)