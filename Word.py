from numpy import *
from cvxSolver import *

class Word:
    def __init__(self, sequence):
        #seqence of permutations
        self.sequence = sequence
        self.flips = []
        self.feasible = "unknown"
        self.constraintMatrix = []

    def toString(self):
        return ""

    def testFeasibility(self):
        cvxSolver.solve(self.constraintMatrix)


    def testPrint(self):
        rtrnString = ""
        for i in range(0, len(self.constraintMatrix)):
            rtrnString += "".join(str(e) + " + " for e in self.constraintMatrix[i]) + " >= " + "0" + "\n"
        return rtrnString





