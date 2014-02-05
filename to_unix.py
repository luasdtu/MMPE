'''
Created on 03/12/2013

@author: MMPE
'''

from cython_compile.cython_compile import cython_compile


@cython_compile
def cython_to_unix(datetimes, fmt):
    from datetime import datetime

    #cdef date zero
    zero = datetime.utcfromtimestamp(0)
    return [(datetime.strptime(dt, fmt) - zero).total_seconds() for dt in datetimes]



