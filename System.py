from numpy import *
from Word import *
from Permutation import *

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
            newRow[symbol.sigma(i+1)] = 1
            newRow[symbol.sigma(i)] = -1
            constraintMatrix.append(newRow)
            constraintVector.append(0)
        #for now, we are NOT going to use agents for 0 and 1 in lieu of 0 < x < 1 explicit constraint
        #first cell greater than 0
        newRow = System.makeZeros(symbol.dim())
        newRow[0] = 1
        constraintMatrix.append(newRow)
        constraintVector.append(0)
        #second cell less than 1
        newRow = System.makeZeros(symbol.dim())
        newRow[0] = -1
        constraintMatrix.append(newRow)
        constraintVector.append(-1)
        temp.constraintMatrix = constraintMatrix
        temp.constraintVector = constraintVector
        return temp


    def concat(self, w1, w2, intermediateFlip):
        temp = Word()
        temp.sequence = []
        temp.sequence.extend(w1.sequence)
        temp.sequence.extend(w2.sequence)
        temp.flips.extend(w1.flips) #append flips of first piece
        temp.flips.append(intermediateFlip) #for now, we know the middle flip
        temp.flips.extend(w2.flips) #append flips of second piece

        #todo: compute constraints and map

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
        permutation = [3,1,2,4,0]
        p1 = Permutation(permutation)
        print "trajectory for test case:"
        print phi(p1)
        system = System(5, phi)
        w1 = system.word(p1)
        print "word constraints"
        print w1.testPrint()

    @staticmethod
    def makeZeros(n):
        temp = []
        for i in range(0,n):
            temp.append(0)
        return temp



System.test()





