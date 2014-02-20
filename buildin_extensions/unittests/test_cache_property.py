'''
Created on 08/11/2013

@author: mmpe
'''
import unittest

from buildin_extensions.dual_key_dict import DualKeyDict
from buildin_extensions.cache_property import set_cache_property
import time
from functions.timing import get_time
import multiprocessing

class Example(object):
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)

        set_cache_property(self, "test", self.slow_function)
        set_cache_property(self, 'pool', lambda : multiprocessing.Pool(20))

    def slow_function(self):
        time.sleep(1)
        return 1

    @get_time
    def prop(self, prop):
        return getattr(self, prop)

def f(x):
    return x ** 2

class TestCacheProperty(unittest.TestCase):
    def setUp(self):
        pass

    def testcache_property_test(self):
        e = Example()
        self.assertAlmostEqual(e.prop("test")[1], 1, 2)
        self.assertAlmostEqual(e.prop("test")[1], 0, 2)

    def testcache_property_pool(self):
        e = Example()
        print e.prop("pool")
        print e.prop("pool")
#
#        pool, t = get_time(multiprocessing.Pool)(processes=4)
#        print t
#        time.sleep(1)
#        print get_time(pool.map)(f, range(10))
        print get_time(e.pool.map)(f, range(10))
        #self.assertAlmostEqual(e.prop("pool")[1], 1, 3)
        #self.assertAlmostEqual(e.prop("pool")[1], 0, 3)




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
