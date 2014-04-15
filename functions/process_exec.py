'''
Created on 10/03/2014

@author: MMPE
'''

from __future__ import division, absolute_import, unicode_literals
import os
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass
DEBUG = False
def pexec(args, cwd=None):
    """
    usage: errorcode, stdout, stderr = pexec("MyProgram.exe arg1, arg2")

    """
    import subprocess
    if not isinstance(args, (list, tuple)):
        args = [args]
    args = [str(arg) for arg in args]
    for i in range(len(args)):
        if os.path.exists(args[i]):
            args[i] = str(args[i]).replace('/', os.path.sep).replace('\\', os.path.sep).replace('"', '')
    if DEBUG:
        comspec = os.environ.get("COMSPEC", "cmd.exe")

        print ("Executing: %s" % '{} /c "{}"'.format (comspec, subprocess.list2cmdline(args)))
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd)
    stdout, stderr = proc.communicate()
    errorcode = proc.returncode
    return errorcode, stdout, stderr
