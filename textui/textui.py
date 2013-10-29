
from __future__ import division, print_function, absolute_import, \
    unicode_literals
import sys
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass

class DaemonUI():

    def progress_iterator(self, iterator, text="Working... Please wait", parent=None, allow_cancel=True):
        return iterator

    def exec_long_task(self, text, allow_cancel, task, *args, **kwargs):
        return task(*args, **kwargs)

    def show_error(self, msg, title="Error"):
        pass

    def show_message(self, msg, title=""):
        pass




class TextUI(DaemonUI):


    def progress_iterator(self, iterator, text="Working... Please wait", parent=None, allow_cancel=True):
        it = iter(iterator)
        if it.__length_hint__() > 0:
            print (text)
            sys.__stdout__.flush()
            m = it.__length_hint__()
            for n, v in enumerate(it):
                if n % 100 == 99:
                    print()
                print (".", end="")
                yield(v)
            print()

    def exec_long_task(self, text, allow_cancel, task, *args, **kwargs):
        print (text)
        return task(*args, **kwargs)

    def show_error(self, msg, title="Error"):
        print(title, msg)

    def show_message(self, msg, title=""):
        if title != "":
            print ("%s\n%s\n%s" % (title, "-"*len(title), msg))
        else:
            print (msg)


