import numpy as np
from Word import *
from Permutation import *
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
        temp.map = identity(symbol.dim())
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
        temp.constraintMatrix = constraintMatrix
        temp.constraintVector = constraintVector
        return temp


    def concat(self, w1, w2, intermediateFlip):
        temp = Word([])
        temp.sequence = []
        temp.sequence.extend(w1.sequence)
        temp.sequence.extend(w2.sequence)
        temp.flips.extend(w1.flips) #append flips of first piece
        temp.flips.append(intermediateFlip) #for now, we know the middle flip
        temp.flips.extend(w2.flips) #append flips of second piece

        #todo: compute constraints and map
        map1 = np.matrix(w1.map)
        map2 = np.matrix(w2.map)
        constraintMat1 = np.matrix(w1.constraintMatrix)
        constraintMat2 = np.matrix(w2.constraintMatrix)

        preimage = constraintMat2 * map1
        finalConstraintMat = copy.deepcopy(np.array(constraintMat1).tolist())
        finalConstraintMat.extend(np.array(preimage).tolist())
        print finalConstraintMat
        finalConstraintVect = copy.deepcopy(w1.constraintVector)
        finalConstraintVect.extend(w2.constraintVector)
        temp.constraintMatrix = finalConstraintMat
        temp.constraintVector = finalConstraintVect


        #1: find map of first word
        #2: compute preimage of dom(w2) (just multiply to right of constraint matrix)
        #3: intersect with dom(w1) (just concat)

        #map
        temp.map = np.array(map2 * map1).tolist()
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
        permutation1 = [3,1,2,4,0]
        p1 = Permutation(permutation1)
        permutation2 = [3,1,4,2,0]
        p2 = Permutation(permutation2)
        permutation3 = [3,1,2,0,4]
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
        print w2.testPrint()
        print w2.testFeasibility()
        w3 = system.concat(w1,w3,"(4,0)")
        print w3.constraintMatrix
        print w3.testPrint()
        print w3.testFeasibility()

    @staticmethod
    def makeZeros(n):
        temp = []
        for i in range(0,n):
            temp.append(0.0)
        return temp



System.test()





