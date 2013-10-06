from numpy import *
from cvxSolver import *

class Word:
    def __init__(self, sequence):
        #seqence of permutations
        self.sequence = sequence
        self.flips = []
        self.feasible = "unknown"
        self.set = []
        self.map = []

    def toString(self):
        return ""

    def testFeasibility(self):
        result = cvxSolver.solve(self.set)
        return (result['status']=='optimal')

    def testPrint(self):
        return self.set.A

    def lastInSequence(self):
        return self.sequence[len(self.sequence)-1]
        





