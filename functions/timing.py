from six import exec_
import time
import inspect
def get_time(f):
    def wrap(*args, **kwargs):
        t = time.clock()
        res = f(*args, **kwargs)
        return res, time.clock() - t
    w = wrap
    w.__name__ = f.__name__
    return w


def print_time(f):
        def wrap(*args, **kwargs):
            t = time.time()
            res = f(*args, **kwargs)
            print ("%-12s\t%.3fs" % (f.__name__, time.time() - t))
            return res
        w = wrap
        w.__name__ = f.__name__
        return w


def print_line_time(f):
        def wrap(*args, **kwargs):
            arg_names, varargs, varkw, defaults = inspect.getargspec(f)
            kwargs[varargs] = args[len(arg_names):]
            kwargs[varkw] = {}
            for k, v in kwargs.items():
                if k not in tuple(arg_names) + (varargs, varkw):
                    kwargs.pop(k)
                    kwargs[varkw][k] = v
            if defaults:
                kwargs.update(dict(zip(arg_names[::-1], defaults[::-1])))
            kwargs.update(dict(zip(arg_names, args)))


            lines = inspect.getsourcelines(f)[0][2:]
            tcum = time.clock()
            locals = kwargs
            gl = f.__globals__

            for l in lines:
                tline = time.clock()
                exec_(l.strip(), locals, gl)  #res = f(*args, **kwargs)
                print ("%.3fs\t%.3fs\t%s" % (time.clock() - tline, time.clock() - tcum, l.strip()))
        w = wrap
        w.__name__ = f.__name__
        return w
