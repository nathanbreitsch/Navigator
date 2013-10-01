__author__ = 'NathanBreitsch'
from cvxopt import matrix, solvers

class cvxSolver:
    @staticmethod
    def solve(m,bIn):
        #build in circle constraints
        numRows = len(m)
        numCols = len(m[0])


        newRow = cvxSolver.makeZeros(len(m[0]))

        A = matrix(m).trans()
        print bIn
        b = matrix(bIn)
        #b = matrix(cvxSolver.makeZeros(numRows))
        c = matrix(cvxSolver.makeZeros(numCols))
        sol=solvers.lp(c,A,b)
        return sol


    @staticmethod
    def makeZeros(n):
        temp = []
        for i in range(0,n):
            temp.append(0.0)
        return temp

    @staticmethod
    def test():
        A = matrix([ [-1.0, -1.0, 0.0, 1.0], [1.0, -1.0, -1.0, -2.0] ])
        print A
        b = matrix([ 1.0, -2.0, 0.0, 4.0 ])
        print b
        c = matrix([ 2.0, 1.0 ])
        print c
        sol=solvers.lp(c,A,b)


cvxSolver.test()

