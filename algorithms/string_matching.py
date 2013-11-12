# This Python file uses the following encoding: cp1252
'''
Created on 11/11/2013

@author: mmpe
'''

from __future__ import division, print_function, absolute_import, \
    unicode_literals

from heapq import heappush, heappop
import sys

from cython_compile.tests.mytimeit import print_time
import numpy as np


try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass

step = 0
score = {('A', 'a'): 0.5}
board = {}
def match2(A, B):
    global step, board
    step += 1
    #print (A, B)
    if (A, B) in board:
        return board[(A, B)]
    if len(A) == 0 or len(B) == 0:
        s = 0
    elif A[0] == B[0]:
        s = 1 + match2(A[1:], B[1:])
    else:
        s = max(match2(A[1:], B), match2(A, B[1:]))
    board[(A, B)] = s
    return s

class Score(object):
    def __init__(self):
        pass

    def get_score(self, a, b):
        if a == b:
            return 1
        elif a.lower() == b.lower():
            return 0.9
        else:
            return 0

class StringMatch(object):
    def __init__(self, score_function):
        self.score_function = score_function

    def get_score(self, A, B):
        scoreboard = np.zeros((len(A) + 1 , len(B) + 1))
        for i, a in enumerate(A):
            for j, b in enumerate(B):
                score = self.score_function(a, b)
                if score > 0:
                    scoreboard[i, j] = scoreboard[i - 1, j - 1] + score
                else:
                    #penalty for skipping a character
                    scoreboard[i, j] = max(scoreboard[i - 1, j], scoreboard[i, j - 1]) - 1 / (len(A) + len(B))
#        print ("%s[%s], %s[%s]: %.3f" % (A, a, B, b, scoreboard[i, j]))
#        print ("\n".join([str(["%.3f" % v for v in row]) for row in scoreboard]))
#        print ()
        return scoreboard[i, j]

    def score_lst_sorted(self, string, lst, thresshold=0, include_scores=False):
        score_lst = []
        for l in lst:
            score = self.get_score(string, l) / len(string)
            if score >= thresshold:
                heappush(score_lst, (-score, l))
        if include_scores:
            return [(-score, string) for score, string in [heappop(score_lst) for _ in range(len(score_lst))]]
        else:
            return [string for _, string in [heappop(score_lst) for _ in range(len(score_lst))]]

    def score_dict(self, string, lst, thresshold=0):
        score_dict = {}
        for l in lst:
            score_dict[l] = self.get_score(string, l) / len(string)
        return score_dict

class SimpleMatch(StringMatch):
    def __init__(self):
        StringMatch.__init__(self, lambda a, b : a == b)

class IgnoreCaseMatch(StringMatch):
    def __init__(self):
        StringMatch.__init__(self, lambda a, b : a == b or a.lower() == b.lower())


class SmartMatch(StringMatch):

    def __init__(self, special_scores=[]):
        self.special_scores = {}
        for a, b, score in special_scores:
            if a > b:
                a, b = b, a
            if a not in self.special_scores:
                self.special_scores[a] = {}
            self.special_scores[a][b] = score

        def score_function(a, b):
            if a == b:
                return 1
            elif a.lower() == b.lower():
                return 0.9
            try:
                if a > b:
                    a, b = b, a
                return self.special_scores[a][b]
            except KeyError:
                return .000
        StringMatch.__init__(self, score_function)



#print (SmartMatch([(u"ø", "o", 1)]).sort_lst("Ford", ["Porche", "ford", "opel", "Opel", "Fo rd", "Førd"], .3))
