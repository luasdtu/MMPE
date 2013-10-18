'''
Created on 06/09/2013

@author: Mads M. Pedersen (mmpe@dtu.dk)
'''
from __future__ import division, print_function, absolute_import, unicode_literals
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass

print ("Hello world")
while 1:
    input = raw_input(">>")
    if input == "quit()": break
    try:
        exec(input)
    except Exception as e:
        print (str(e))
