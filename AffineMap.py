__author__ = 'NathanBreitsch'
from numpy import *

class AffineMap:
    def __init__(self,A,b):
        self.A = matrix(A)
        self.b = matrix(b)
        if self.b.shape[0] != self.A.shape[0]:#its fucking counterintuitive, but shape[0] gives cols in A and rows in b
            self.b = transpose(self.b)


    @staticmethod
    def compose(m1, m2):
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

