__author__ = 'NathanBreitsch'
from cvxopt import matrix
from numpy import *


class ConvexSet:
    def __init__(self,A,b):
        self.A = matrix(A)
        self.b = matrix(b)
        print self.b.shape[1]
        if self.b.shape[0] != self.A.shape[0]:#its fucking counterintuitive, but shape[0] gives cols in A and rows in b
            self.b = transpose(self.b)


    @staticmethod
    def intersect(cs1, cs2):
        tempA = concatenate((cs1.A,cs2.A))
        tempb = concatenate((cs1.b,cs2.b))
        temp = ConvexSet(tempA,tempb)
        #temp.A = tempA
        #temp.b = tempb
        return temp



