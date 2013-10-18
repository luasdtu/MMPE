d = None
d = dir()

from mymodule import p

__all__ = [m for m in set(dir()) - set(d)]
