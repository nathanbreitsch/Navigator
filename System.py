import numpy as np
from Word import *
from Permutation import *
from ConvexGeometry import *
import copy

class System:

    #a system is defined by dimension and phi function
    def __init__(self, dim, phi):
        self.dim = dim
        self.phi = phi


    #make a one-symbol word from given symbol
    def word(self, symbol):
        sequence = []
        sequence.append(symbol)
        temp = Word(sequence)
        #todo: compute constraints and map
        #just make map the identity
        temp.map = AffineMap(identity(symbol.dim()), System.makeZeros(symbol.dim()))
        #next make the constraints
        constraintMatrix = []
        constraintVector = []
        for i in range(0, symbol.dim()-1):
            newRow = System.makeZeros(symbol.dim())
            newRow[symbol.sigma(i+1)] = 1.0
            newRow[symbol.sigma(i)] = -1.0
            constraintMatrix.append(newRow)
            constraintVector.append(0.0)
        #for now, we are NOT going to use agents for 0 and 1 in lieu of 0 < x < 1 explicit constraint
        #actually, we can build these constraints into the solver
        #first cell greater than 0
        newRow = System.makeZeros(symbol.dim())
        newRow[0] = 1.0
        constraintMatrix.append(newRow)
        constraintVector.append(0.0)
        #second cell less than 1
        newRow = System.makeZeros(symbol.dim())
        newRow[symbol.dim()-1] = -1.0
        constraintMatrix.append(newRow)
        constraintVector.append(-1.0)
        temp.set = ConvexSet(constraintMatrix, constraintVector)
        return temp


    def concat(self, w1, w2, intPerm):

        #todo compute intermediate map
        phi = self.phi(w1.lastInSequence())
        intermediateMatrix = []
        intermediateVector = []
        print "phi"
        print phi

        if intPerm == "R":
            #rotation case
            print "rotation"
            for i in range(0, self.dim - 1):
                speedRatio = phi[i]/phi[w1.lastInSequence().sigmaInv(self.dim-1)]
                temp = System.makeZeros(self.dim)
                temp[i] += 1
                temp[w1.lastInSequence().sigmaInv(self.dim-1)] -= phi[i] * speedRatio
                intermediateMatrix.append(temp)
            intermediateMatrix.append(System.makeZeros(self.dim))
            for i in range(0, self.dim):
                intermediateVector.append(speedRatio)
        else:
            #transposition case
            print "transposition"
            for i in range(0, self.dim):
                speedRatio = phi[i]/(phi[intPerm[1]] - phi[intPerm[0]])
                print "speedRatio"
                print speedRatio
                temp = System.makeZeros(self.dim)
                temp[i] += 1
                temp[intPerm[0]] += phi[i] * speedRatio
                temp[intPerm[1]] -= phi[i] * speedRatio
                intermediateMatrix.append(temp)
            intermediateVector = System.makeZeros(self.dim)
            print intermediateMatrix

        intermediateMap = AffineMap(intermediateMatrix, intermediateVector)


        temp = Word([])
        temp.sequence = []
        temp.sequence.extend(w1.sequence)
        temp.sequence.extend(w2.sequence)
        temp.flips.extend(w1.flips) #append flips of first piece
        temp.flips.append(intPerm) #for now, we know the middle flip
        temp.flips.extend(w2.flips) #append flips of second piece

        #todo: compute constraints and map
        temp.map = AffineMap.compose(intermediateMap,w1.map)
        temp.set = ConvexSet.intersect(w1.set, ConvexGeometry.preImage(temp.map, w2.set))
        temp.map = AffineMap.compose(w2.map, temp.map)
        print temp.map.A
        return temp


    @staticmethod
    def test():
        def phi(perm):
            #let 3 ~ s, 4 ~ r

            sIndex = perm.sigmaInv(3)

            temp = []
            for i in range(0,3):
                if perm.sigmaInv(i) < perm.sigmaInv(4): #case: not in R
                    temp.append(1)
                else: #case in R
                    temp.append(1-sIndex * (1.0/10.0))
            for i in range(3,5): #parameters
                temp.append(0)
            return temp
        permutation1 = [1,3,2,4,0]
        p1 = Permutation(permutation1)
        permutation2 = [1,3,4,2,0]
        p2 = Permutation(permutation2)
        permutation3 = [1,3,2,0,4]
        p3 = Permutation(permutation3)
        print("trajectories for test case")
        print phi(p1)
        print phi(p2)
        system = System(5, phi)
        w1 = system.word(p1)
        w2 = system.word(p2)
        w3 = system.word(p3)
        print("word constraints")
        print w1.testPrint()
        print w1.testFeasibility()
        print w3.testPrint()
        print w3.testFeasibility()
        w3 = system.concat(w3,w1,(4,0))
        print w3.testPrint()
        print w3.testFeasibility()

    @staticmethod
    def makeZeros(n):
        temp = []
        for i in range(0,n):
            temp.append(0.0)
        return temp



System.test()





