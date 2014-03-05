
from __future__ import division, print_function, absolute_import, \
    unicode_literals
import sys
from ui.daemon_ui import DaemonUI
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass


class TextOutputUI(DaemonUI):

    def show_message(self, msg, title="Information"):
        if title != "":
            print ("%s\n%s\n%s" % (title, "-"*len(title), msg))
        else:
            print (msg)

    def show_warning(self, msg, title="Warning"):
        print ("%s\n%s\n%s" % (title, "-"*len(title), msg))

    def show_text(self, text):
        print (text)

class TextInputUI(object):
    def get_confirmation(self, title, msg):
        raise NotImplementedError

    def get_string(self, title, msg):
        raise NotImplementedError

    def get_open_filename(self, title="Open", filetype_filter="*.*", file_dir=None, selected_filter=None):
        raise NotImplementedError
    def get_save_filename(self, title, filetype_filter, file_dir=None, selected_filter=None):
        raise NotImplementedError


    def get_open_filenames(self, title, filetype_filter, file_dir=None):
        raise NotImplementedError

    def get_foldername(self, title='Select directory', file_dir=None):
        raise NotImplementedError



class TextStatusUI(object):

    def progress_iterator(self, sequence, text="Working... Please wait", allow_cancel=True):
        it = iter(sequence)
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

    def start_wait(self):
        print ("Working please wait")

    def end_wait(self):
        print ("finish")



class TextUI(TextOutputUI, TextInputUI, TextStatusUI):
    pass
