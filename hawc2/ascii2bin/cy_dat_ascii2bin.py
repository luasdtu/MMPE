from array import array
import cython
import math
import multiprocessing
import numpy as np
import time
from cython_compile import cython_compile_autodeclare, cython_compile
# cimport numpy as np


def readfile(ascii_filename):
    infile = open(ascii_filename, 'r')
    lines = infile.readlines()
    return lines

def max_numpy_size():
    above = 10000
    below = 0
    while above - below > 1:
        n = below + (above - below) / 2
        try:
            d = np.empty((n, 1024 * 1024), dtype=np.byte)
            del d
            below = n
        except:
            above = n
    return below * 1024 ** 2

@cython.ccall
def dat_ascii2bin_progress(ascii_filename, bin_filename, size, ui):
    #cdef int x1, x2, ncols, from_col, to_col
    #cdef float scale_factor
    #cdef np.ndarray[np.float64_t,ndim=1] nparr
    lines = ui.exec_long_task("Read file", True, readfile, ascii_filename)
    ncols = min(size[1], max_numpy_size() // (size[0] * 8) // 2)

    if ncols < 1:
        ui.show_error("File cannot be converted. Out of memory\nAvailable continuous memory: \t%d mb\nRequired continuous: \t%d mb" % (max_numpy_size(), (size[0] * 8) / 1024 ** 2))
        return
    else:
        nparr = np.empty(size[0], dtype=np.float64)
    outfile = open(bin_filename, 'wb')
    scale_factors = []
    for from_col in xrange(0, size[1], ncols):
        txt = "columns %d-%d out of %d" % (from_col, min(size[1], from_col + ncols), size[1])
        to_col = min(size[1], from_col + ncols)
        arrays = []

        for x1 in ui.progress_iterator(xrange(from_col * 13, 13 * to_col, 13), "Read " + txt, ui, True,):
            x2 = x1 + 14
            arrays.append([float(line[x1:x2]) for line in lines])

        for arr in ui.progress_iterator(arrays, "Write " + txt, ui, True):
            nparr[:] = np.array(arr, dtype=np.float64)
            del arr
            scale_factor = max(abs(nparr)) / 32000
            # avoid dividing by zero
            if scale_factor > 0:
                nparr /= scale_factor
            #round and write
            np.round(nparr).astype(np.int16).tofile(outfile)
            scale_factors.append(scale_factor)
        del arrays
    outfile.close()
    return scale_factors

