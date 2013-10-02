__author__ = 'NathanBreitsch'
from cvxopt import matrix
from numpy import *


class ConvexSet:
    def __init__(self,A,b):
        self.A = matrix(A)
        self.b = transpose(matrix(b))

    @staticmethod
    def intersect(cs1, cs2):
        tempA = concatenate(cs1.A,cs2.A)
        tempb = concatenate(cs1.b,cs2.b)
        return ConvexSet(tempA,tempb)


