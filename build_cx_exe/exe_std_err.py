import os
import win32ui
class ExeStdErr(object):
    user_informed = False
    def __init__(self):
        try:
            os.remove("std_err.out")
        except:
            pass

    def write(self, s):
        try:
            with open("std_err.out", 'a') as fid:
                fid.write(s)
            print  "Error", s,
            if not self.user_informed:
                win32ui.MessageBox("An error has occured. The error message has been written to:\n%s" % os.path.realpath('std_err.out'), "Error occured")
                self.user_informed = True
        except:
            pass
