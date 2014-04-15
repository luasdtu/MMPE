import os

class ExeStdOut(object):
    def __init__(self, *args):
        self.filename = 'std_out.out'
        if args:
            self.write(" ".join([str(arg) for arg in args]))

    def write(self, s):
        try:
            with open(os.path.realpath(self.filename), 'a') as fid:
                fid.write(s + "\n---------\n")
            print  (s)
        except:
            pass

    def clear(self):
        try:
            with open(os.path.realpath(self.filename), 'w'):
                pass
        except:
            pass

