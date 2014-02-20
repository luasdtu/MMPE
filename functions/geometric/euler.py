'''
Created on 15/01/2014

@author: MMPE
'''

from __future__ import division, absolute_import, unicode_literals
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass

from functions.geometric import deg, rad
import numpy as np



def euler2A(euler_param):
    e = euler_param
    return np.array([[e[0] ** 2 + e[1] ** 2 - e[2] ** 2 - e[3] ** 2, 2 * (e[1] * e[2] + e[0] * e[3]) , 2 * (e[1] * e[3] - e[0] * e[2]) ],
                         [2 * (e[1] * e[2] - e[0] * e[3]), e[0] ** 2 - e[1] ** 2 + e[2] ** 2 - e[3] ** 2, 2 * (e[2] * e[3] + e[0] * e[1]) ],
                         [2 * (e[1] * e[3] + e[0] * e[2]), 2 * (e[2] * e[3] - e[0] * e[1]), e[0] ** 2 - e[1] ** 2 - e[2] ** 2 + e[3] ** 2]]).T

def A2xyz(A):
    if abs(A[2, 0]) != 1:
        y = -np.arcsin(A[2, 0])
        x = np.arctan2(A[2, 1] / np.cos(y), A[2, 2] / np.cos(y))
        z = np.arctan2(A[1, 0] / np.cos(y), A[0, 0] / np.cos(y))
    else:
        z = 0
        if A[2, 0] == -1:
            y = np.pi / 2
            x = z + np.arctan(A[0, 1], A[0, 2])
        else:
            y = -np.pi / 2
            x = -z + np.arctan(-A[0, 1], -A[0, 2])
    return np.array([y, x, z])

def xyz2euler(x, y, z):
    return np.array([np.cos(.5 * (z + x)) * np.cos(.5 * y),
                     np.cos(.5 * (z + x)) * np.sin(.5 * y),
                     np.sin(.5 * (z + x)) * np.sin(.5 * y),
                     np.sin(.5 * (z + x)) * np.cos(.5 * y)])

def xyz2A(x, y, z):
    return euler2A(xyz2euler(x, y, z))

def euler2xyz(euler):
    return A2xyz(euler2A(euler))

def A2euler(A):
    return xyz2euler(*A2xyz(A))

def euler2angle(euler):
    return np.arccos(euler[0]) * 2

def euler2gl(euler):
    return np.r_[deg(euler2angle(euler)), euler[1:]]
