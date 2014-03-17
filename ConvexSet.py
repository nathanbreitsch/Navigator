__author__ = 'NathanBreitsch'
from cvxopt import matrix
import numpy as np
from rationalApprox import simpleApprox, intApprox
import cdd



class ConvexSet:
    def __init__(self,A ,b ):



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

    #pycddlib wants the form (b,-A) for some fucked up reason
    def getVertices(self):
        tableau = np.concatenate((self.b, np.multiply(-1, self.A)), axis=1) #join b to the right of a to make tableau
        mat = cdd.Matrix(tableau.tolist())
        #mat.canonicalize()#get rid of redundencies
        mat.rep_type = cdd.RepType.INEQUALITY
        poly = cdd.Polyhedron(mat)
        vertices = poly.get_generators()
        print poly.get_inequalities()
        return vertices

    #pycddlib wants the form (b,-A) for some fucked up reason
    def getInequalities(self):
        tableau = np.concatenate((self.b, np.multiply(-1, self.A)), axis=1) #join b to the right of a to make tableau
        mat = cdd.Matrix(tableau.tolist())
        #mat.canonicalize()#get rid of redundencies
        poly = cdd.Polyhedron(mat)
        return poly.get_inequalities()

    def writeVertices(self, path):
        f = open(path,"w")
        f.write(str(self.getVertices()))
        #f.write(self.getJson())
        f.close()

    #return dictionary representing the object
    def getDict(self, info):
        stringForm = str(self.getVertices())
        vector = stringForm.split("\n")
        matrix = []
        for line in vector[3:-1]:
            line = line.replace("  ", " ")
            line = line.replace("  ", " ")
            line = line.replace("  ", " ")
            array = line.split(" ")[2:]
            matrix.append(array)
        dict = {"points": matrix, "info": info}
        return dict

    #returns representation of crosssection (certain variables are fixed)
    #@param values: value at which to fix each variable, '?' if not projected
    def standardCrossSection(self, values):
        AxSection = self.A[:, [index for index in range(0, len(values)) if values[index] == '?']]
        bxSection = self.b - sum(values[index] * self.A[:, index] for index in range(0, len(values)) if values[index]!='?')
        unboundConstraints = ConvexSet(AxSection, bxSection)
        numCols = AxSection.shape[1]
        #bound values between zero and one
        #boundConstraints = ConvexSet.intersect(unboundConstraints, ConvexSet.makeSquareConstraints(numCols))
        return unboundConstraints
        #return boundConstraints

    def ineRepresentation(self):
        numRows = self.A.shape[0]
        numCols = self.A.shape[1] + 1
        parameters = str(numRows) + " " + str(numCols) + " rational"
        inequalities = ""
        for i in range(0, numRows):
            rowString = ""
            for j in range(0, numCols-1):
                rowString += intApprox(self.A[i, j], 8) + " "
            rowString += intApprox(self.b[i, 0], 8)
            inequalities += rowString + "\n"


        contents = "H-representation\nbegin\n" + parameters + "\n" + inequalities + "end"
        return contents

    def writeIne(self, name, path):
        contents = self.ineRepresentation()
        f = open(path, "w")
        f.write(name + "\n" + str(self.getInequalities()))
        f.close()

    @staticmethod
    def makeSquareConstraints(numCols):
        id = np.identity(numCols)
        b0 = np.zeros(numCols)
        b1 = np.ones(numCols)
        lower = ConvexSet(np.multiply(-1, id), b0)
        upper = ConvexSet(id, b1)
        #testing

        return ConvexSet.intersect(lower, upper)

    @staticmethod
    def intersect(cs1, cs2):
        tempA = np.concatenate((cs1.A, cs2.A))
        tempb = np.concatenate((cs1.b, cs2.b))
        temp = ConvexSet(tempA, tempb)
        #temp.A = tempA
        #temp.b = tempb
        return temp

    @staticmethod
    def testStandardCrossSection():
        #we start with a unit square
        A = [[0,-1],[0,1],[-1,0],[1,0]]
        b = [0,1,0,1]
        set = ConvexSet(A,b)
        #we take a horizontal cross section at y = 1/2
        selection = ['?',0.5]
        crossSection = set.standardCrossSection(selection)
        print crossSection.A
        print crossSection.b


#print ConvexSet.makeSquareConstraints(3).A.tolist()
#print ConvexSet.makeSquareConstraints(3).b.tolist()
#print ConvexSet.makeSquareConstraints(3).getVertices()

ConvexSet.testStandardCrossSection()
