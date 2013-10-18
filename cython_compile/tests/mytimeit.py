import time
def get_time(f):
    def wrap(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        return res, time.time() - t
    w = wrap
    w.__name__ = f.__name__
    return w


def print_time(f):
        def wrap(*args, **kwargs):
            t = time.time()
            res = f(*args, **kwargs)
            print "%-12s\t%.3fs" % (f.__name__, time.time() - t)
            return res
        w = wrap
        w.__name__ = f.__name__
        return w
