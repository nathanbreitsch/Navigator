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

    #returns representation of crosssection (certain variables are fixed)
    #@param values: value at which to fix each variable, '?' if not projected
    def standardCrossSection(self, values):
        AxSection = self.A[:, [index for index in range(0, len(values)) if values[index] == '?']]
        bxSection = self.b - sum(values[index] * self.A[:, index] for index in range(0, len(values)) if values[index]!='?')
        return ConvexSet(AxSection, bxSection)

    def toIneFile(self):
        numRows = len(self.A)
        numCols = len(self.A[0]) + 1
        parameters = numRows + " " + numCols + " rational"
        inequalities = ""
        for i in range(0, numRows):
            rowString = ""
            for j in range(0, numCols):
                rowString += str(self.A[i][j]) + " "
            rowString += str(self.b[i])
            inequalities += rowString + "\n"


        contents = "name\nH-representation\nbegin\n" + parameters + "\n" + inequalities + "end"
        #f = open("./data/", "w")
        #f.write(contents)
        #f.close()

    @staticmethod
    def intersect(cs1, cs2):
        tempA = np.concatenate((cs1.A, cs2.A))
        tempb = np.concatenate((cs1.b, cs2.b))
        temp = ConvexSet(tempA, tempb)
        #temp.A = tempA
        #temp.b = tempb
        return temp




