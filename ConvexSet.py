__author__ = 'NathanBreitsch'
from cvxopt import matrix
import numpy as np



class ConvexSet:
    def __init__(self,A,b):
        self.A = np.matrix(A)
        self.b = np.matrix(b)
        if self.b.shape[0] != self.A.shape[0]:#its counterintuitive, but shape[0] gives cols in A and rows in b
            self.b = np.transpose(self.b)

    def __call__(self):
        return ConvexSet(self.A, self.b)

    #im doing this until I figure out why the static method won't work
    def intersect(self, cs1, cs2):
        tempA = np.concatenate((cs1.A, cs2.A))
        tempb = np.concatenate((cs1.b, cs2.b))
        temp = ConvexSet(tempA, tempb)
        #temp.A = tempA
        #temp.b = tempb
        return temp

    def serialize(self):
        representation = {}
        representation["A"] = self.A.tolist()
        representation["b"] = self.b.tolist()

    def standardCrossSection(self, c):
        assert(len(c) == len(self.A[0]))

    @staticmethod
    def intersect(cs1, cs2):
        tempA = np.concatenate((cs1.A, cs2.A))
        tempb = np.concatenate((cs1.b, cs2.b))
        temp = ConvexSet(tempA, tempb)
        #temp.A = tempA
        #temp.b = tempb
        return temp



