'''
Created on 18/03/2014

@author: mmpe
'''


from bbfreeze import Freezer
f = Freezer("hello-world-1.0", includes=("_strptime",))
f.addScript("hello.py")
#f.addScript("hello-version.py")
f()  # starts the freezing process
