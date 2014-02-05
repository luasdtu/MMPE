import os

import psutil


class MemoryUsage(object):
    def __init__(self):
        self.init_usage = self._usage()

    def usage(self):
        return self._usage() - self.init_usage

    def _usage(self):
        return psutil.Process(os.getpid()).get_memory_info()[0] / 1024 ** 2
mem = MemoryUsage()