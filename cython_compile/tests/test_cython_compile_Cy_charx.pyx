import cython
import numpy as np
cimport numpy as np
cpdef char* Cy_charx(char* c):
    return c.upper()
