'''
Created on 10/04/2014

@author: MMPE
'''

from __future__ import division, absolute_import, unicode_literals

import inspect
import os
import time
import zipfile


try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass


def class_list(func_path, base_class, exclude_classes=[]):
    exclude_classes.append(base_class)
    class_lst = []

    file_lst = []
    for root, _, files in os.walk(func_path):
        file_lst.extend([os.path.join(root, f) for f in files if f.lower().endswith('.py')])

    if zipfile.is_zipfile('library.zip'):
        z = zipfile.ZipFile('library.zip')
        file_lst.extend([f for f in z.namelist() if f.startswith(func_path)])

    for module_name in [os.path.splitext(f)[0].replace("\\", ".").replace("/", ".") for f in file_lst]:
        t = time.time()
        module = __import__(module_name, {}, {}, ['*'])
        class_lst.extend([cls for cls in module.__dict__.values()
                          if inspect.isclass(cls) and issubclass(cls, base_class) and not cls in exclude_classes])
        if time.time() - t > 0.1:
            print (module_name, time.time() - t)
    return class_lst


def argument_string(func):
    if hasattr(func, 'target_function'):
        func = func.target_function
    try:
        args, varargs, keywords, defaults = inspect.getargspec(func)
        if defaults is not None:
            for nr in range(1, len(defaults) + 1):
                d = defaults[-nr]
                if isinstance(d, basestring):
                    d = "'%s'" % d
                elif isinstance(d, type):
                    d = str(d).split("'")[1].replace("numpy", "np")
                args[-nr] = "%s=%s" % (args[-nr], d)

        if varargs is not None:
            args.append("*%s" % varargs)

        if keywords is not None:
            args.append("**%s" % keywords)

        if len(args) > 0 and args[0] == 'self':
            return "(%s)" % ", ".join(args[1:])  # remove self
        else:
            return "(%s)" % ", ".join(args)
    except TypeError:
        return ""