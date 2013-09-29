from numpy import *
from SatSolver import *

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
        SatSolver.solve(self.constrintMatrix)


    def testPrint(self):
        rtrnString = ""
        for i in range(0, len(self.constraintVector)):
            rtrnString += "".join(str(e) + " + " for e in self.constraintMatrix[i]) + " >= " + str(self.constraintVector[i]) + "\n"
        return rtrnString





