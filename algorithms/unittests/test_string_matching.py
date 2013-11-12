'''
Created on 11/11/2013

@author: mmpe
'''
import unittest
from algorithms.string_matching import SmartMatch


class Test(unittest.TestCase):





    def testStringMatching2(self):
        lst = SmartMatch([(u"0", "o", 1)]).score_lst_sorted("Ford", ["Porche", "ford", "opel", "Opel", "Fo rd", "F0rd"], .3, False)
        self.assertEqual(['F0rd', 'ford', 'Fo rd', 'Porche'], lst)


    def testStringMatching3(self):
        s1 = SmartMatch().get_score("b", "aaaaaaba")
        s2 = SmartMatch().get_score("b    ", "baaaaaa")
        self.assertTrue(s1 > 0)
        self.assertTrue(s2 > 0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testStringMatching1']
    unittest.main()
