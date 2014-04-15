'''
Created on 06/09/2013

@author: Mads M. Pedersen (mmpe@dtu.dk)
'''
from __future__ import division, print_function, absolute_import, unicode_literals
import time
import sys
import traceback
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass
import numpy

while 1:
    input = raw_input(">>")
    if input == "quit()": break
    if input == "": input = "import pandas"
    try:
        t = time.clock()
        _return_ = None
        if input.strip().startswith("import") or input.strip().startswith("from"):
            exec(input, globals(), locals())
        else:
            exec("print (%s)" % input, globals(), locals())
        print ("%f" % (time.clock() - t))
    except Exception as e:
        print (str(e))
        print (traceback.format_exc())
