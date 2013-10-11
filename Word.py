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
        if self.set == []:
            return False
        else:
            result = cvxSolver.solve(self.set)
            return (result['status']=='optimal')

    def testPrint(self):
        print "constraint A"
        print self.set.A
        print "constraint b"
        print self.set.b
        print "map A"
        print self.map.A

    def lastInSequence(self):
        return self.sequence[len(self.sequence)-1]
        





