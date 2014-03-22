__author__ = 'NathanBreitsch'
from numpy import *

class AffineMap:
    def __init__(self,A,b):


        self.A = matrix(A)
        self.b = matrix(b)
        if self.b.shape[0] != self.A.shape[0]:#its fucking counterintuitive, but shape[0] gives cols in A and rows in b
            self.b = transpose(self.b)

    def scale(self, scalar):
        tempA = copy.deepcopy(self.A)
        tempb = copy.deepcopy(self.b)
        for i in range(0, len(A)):
            for j in range(0, len(A[0])):
                tempA[i,j] *= scalar
        for i in range(0, len(b)):
            tempb[i] *= scalar

    #returns dictionary representation of map
    def serialize(self):
        representation = {}
        representation["A"] = self.A.tolist()
        representation["b"] = self.b.tolist()
        return representation

    #given dictionary representation, returns map
    @staticmethod
    def deserialize(rep):
        return AffineMap(rep["A"], rep["b"])


    @staticmethod
    def compose(m1, m2):
        #print m1.A
        #print m2.A
        tempA = m1.A * m2.A
        tempb = m1.A*m2.b + m1.b
        return AffineMap(tempA, tempb)

    @staticmethod
    def identity(n):
        A = identity(n)
        b = []
        for i in range(0, n):
            b.append(0)
        return AffineMap(A, b)

