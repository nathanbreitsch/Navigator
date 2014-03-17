import numpy as np
from Word import *
from Permutation import Permutation
from ConvexGeometry import *
import copy

#phi is indexed with innate coordinates
#trans uses order coordinates
#sigma converts innate to order
#sigmaInv converts order to innate
#all constraints of the form Ax <= b
#all constraints use innate coordinates
#all maps use innate coordinates
#all intermediate permutations (transpositions) use order coordinates

class System:

    #a system is defined by dimension and phi function
    def __init__(self, dim, phi):
        self.dim = dim
        self.phi = phi #phi is indexed by innate indices
        self.separationConstraint = System.makeSeparationConstraint(0.001)


    #make a one-symbol word from given symbol
    def word(self, symbol):
        sequence = []
        sequence.append(symbol)
        temp = Word(sequence)
        #todo: compute constraints and map
        #just make map the identity
        temp.map = AffineMap(identity(self.dim), System.makeZeros(self.dim))
        #next make the constraints
        constraintMatrix = []
        constraintVector = []
        for q in range(0, symbol.dim()-1): #cvxopt uses <= constraints by default
            newRow = System.makeZeros(symbol.dim())
            newRow[symbol.sigmaInv(q+1)] = -1.0
            newRow[symbol.sigmaInv(q)] = 1.0
            constraintMatrix.append(newRow)
            constraintVector.append(0.0)
        #for now, we are NOT going to use agents for 0 and 1 in lieu of 0 < x < 1 explicit constraint
        #actually, we can build these constraints into the solver
        #first cell greater than 0
        newRow = System.makeZeros(symbol.dim())
        newRow[symbol.sigmaInv(0)] = -1.0
        constraintMatrix.append(newRow)
        constraintVector.append(0.0)
        #second cell less than 1
        newRow = System.makeZeros(symbol.dim())
        newRow[symbol.sigmaInv(symbol.dim()-1)] = 1.0
        constraintMatrix.append(newRow)
        constraintVector.append(1.0)
        temp.set = ConvexSet(constraintMatrix, constraintVector)
        #separationConstraints if you want them
        #temp.set = ConvexSet.intersect(temp.set, self.separationConstraint)
        return temp

    def invariant(self, perm): #warning: not written generically
        return perm.sigma(3) == 3 and perm.sigma(4) == 4

    def oldconcat(self, w1, w2, intPerm):
        #todo: handle case when things "passing" eachother travel the same speed
        phi = self.phi(w1.lastInSequence())
        intermediateMatrix = []
        intermediateVector = []
        midTraj = w1.lastInSequence()

        if intPerm == "R":
            #rotation case
            criticalIndex = midTraj.sigmaInv(self.dim-1)
            speedDifferential = phi[criticalIndex]
            if speedDifferential == 0:
                #return with null feasibility
                temp = Word([])
                temp.sequence = []
                temp.sequence.extend(w1.sequence)
                temp.sequence.extend(w2.sequence)
                return temp
            for i in range(0, self.dim):
                speedRatio = phi[i]/speedDifferential
                temp = System.makeZeros(self.dim)
                if i != criticalIndex:
                    temp[i] += 1
                    temp[criticalIndex] -= speedRatio
                    intermediateMatrix.append(temp)
                    intermediateVector.append(speedRatio)
                else:
                    intermediateMatrix.append(temp)
                    intermediateVector.append(speedRatio-1)
            print "intermediateMatrix"
            print intermediateMatrix
            print intermediateVector

        else:
            #transposition case
            speedDifferential = phi[midTraj.sigmaInv(intPerm[1])] - phi[midTraj.sigmaInv(intPerm[0])]
            if speedDifferential >= 0:
                #return with null feasibility
                temp = Word([])
                temp.sequence = []
                temp.sequence.extend(w1.sequence)
                temp.sequence.extend(w2.sequence)
                return temp
            for i in range(0, self.dim):
                speedDifferential = phi[midTraj.sigmaInv(intPerm[1])] - phi[midTraj.sigmaInv(intPerm[0])]
                speedRatio = phi[i]/(speedDifferential)
                temp = System.makeZeros(self.dim)
                temp[i] += 1
                temp[midTraj.sigmaInv(intPerm[0])] += speedRatio
                temp[midTraj.sigmaInv(intPerm[1])] -= speedRatio
                intermediateMatrix.append(temp)
            intermediateVector = System.makeZeros(self.dim)

        intermediateMap = AffineMap(intermediateMatrix, intermediateVector)

        temp = Word([])
        temp.sequence = []
        temp.sequence.extend(w1.sequence)
        temp.sequence.extend(w2.sequence)
        temp.flips.extend(w1.flips) #append flips of first piece
        temp.flips.append(intPerm) #for now, we know the middle flip
        temp.flips.extend(w2.flips) #append flips of second piece

        #transform intPerm into static indexing
        if intPerm == "R":
            loggedEvent = "R"
        else:
            index1 = w1.sequence[-1].permutation[intPerm[0]]
            index2 = w1.sequence[-1].permutation[intPerm[1]]
            loggedEvent = [index1,index2]
        temp.eventLog.extend(w1.eventLog)
        temp.eventLog.append(loggedEvent)
        temp.eventLog.extend(w2.eventLog)

        #todo: compute constraints and map
        temp.map = AffineMap.compose(intermediateMap,w1.map)
        temp.set = ConvexSet.intersect(w1.set, ConvexGeometry.preImage(temp.map, w2.set))
        temp.map = AffineMap.compose(w2.map, temp.map)
        return temp

    def concat(self, w1, trans):

        #trans uses order indices rather than innate indices
        currentPermutation = w1.lastInSequence()
        newWord = Word([])
        newWord.sequence.extend(w1.sequence)
        newWord.sequence.append(currentPermutation.transpose(trans))#append the result of the transposition?
        newWord.flips.extend(w1.flips)
        newWord.flips.append(trans)

        frequency = self.phi(currentPermutation) #frequency vector for current permutation

        #new maps
        if (trans == "R"):
            indexFront = 0
            indexBack = currentPermutation.sigmaInv(self.dim - 1)
            fback = frequency[indexBack]
            ffront = 0
            newMatrix = []
            newVector = []
            #cyclic reindex: there is none, we're using innate coordinates
            #just set the xsigmainvn-1 to 0
            for i in range(0, self.dim):#i is innate
                temp = System.makeZeros(self.dim)#zero vector
                if i != currentPermutation.sigmaInv(self.dim - 1):#everywhere except for oscillator hitting 1
                    assert(fback != 0)
                    freqRatio = frequency[i]/fback
                    temp[i] = 1
                    temp[indexBack] -= freqRatio
                    newMatrix.append(temp)
                    newVector.append(freqRatio)
                else: #the row of the oscillator hitting 1, set to zero
                    newMatrix.append(temp)#just zeros
                    newVector.append(0)


        else:
            indexBack = currentPermutation.sigmaInv(trans[0])
            indexFront = currentPermutation.sigmaInv(trans[1])
            fback = frequency[indexBack]
            ffront = frequency[indexFront]
            newMatrix = []
            newVector = System.makeZeros(self.dim)
            for i in range(0, self.dim):#i is innate
                freqRatio = frequency[i]/(fback - ffront)
                temp = System.makeZeros(self.dim)#zero vector
                temp[i] = 1
                temp[indexFront] += freqRatio
                temp[indexBack] -= freqRatio
                newMatrix.append(temp)
        newMap = AffineMap(newMatrix, newVector)

        newWord.map = AffineMap.compose(newMap, w1.map)#i think I should compose from left (check)


        #make row for mainTrans
        mainRow = System.makeZeros(self.dim)
        if trans == 'R':
            tBack = currentPermutation.sigmaInv(self.dim - 1)#innate
            mainRow[tBack] += -1/frequency[tBack]
            mainConstant = 1/frequency[tBack]
        else:
            tFront = currentPermutation.sigmaInv(trans[1])
            tBack = currentPermutation.sigmaInv(trans[0])
            mainRow[tBack] += -1/(frequency[tBack] - frequency[tFront])
            mainRow[tFront] += 1/(frequency[tBack] - frequency[tFront])
            mainConstant = 0

        transpositions = self.admissibleTranspositions(currentPermutation)
        constraintA = []
        constraintb = []
        for competingTrans in transpositions:
            if competingTrans != trans:
                if competingTrans == 'R':
                    ctBack = currentPermutation.sigmaInv(self.dim - 1)#innate
                    competingRow = System.makeZeros(self.dim)
                    competingRow[ctBack] = -1/frequency[ctBack]#temp and frequency use innate indices
                    competingConstant = 1/frequency[ctBack]

                else:
                    q = competingTrans[1]
                    ctBack = currentPermutation.sigmaInv(q-1)
                    ctFront = currentPermutation.sigmaInv(q)
                    competingRow = System.makeZeros(self.dim)#temp will use innate indices since it is used to make constraints
                    assert(frequency[ctBack] != frequency[ctFront])
                    competingRow[ctBack] = -1/(frequency[ctBack] - frequency[ctFront])
                    competingRow[ctFront] = 1/(frequency[ctBack] - frequency[ctFront])
                    competingConstant = 0

                constraintRow = []
                for i in range(0, self.dim):
                    constraintRow.append(mainRow[i] - competingRow[i])
                constraintConstant = competingConstant - mainConstant
                constraintA.append(constraintRow)
                constraintb.append(constraintConstant)




        #append zero row for empty set of constraints
        constraintA.append(System.makeZeros(self.dim))
        constraintb.append(0.0)

        constraintsAtTrans = ConvexSet(constraintA, constraintb)
        constraintsAt0 = ConvexGeometry.preImage(w1.map, constraintsAtTrans)
        newWord.set = ConvexSet.intersect(constraintsAt0, w1.set)

        return newWord

    #return a list containing all permissible transpositions
    #transposition is permissable if fback > ffront
    def admissibleTranspositions(self, perm):
        admissible = []
        frequency = self.phi(perm)
        if (frequency[perm.sigmaInv(self.dim - 1)] > 0):
            admissible.append("R")
        for i in range(1, self.dim):
            fback = frequency[perm.sigmaInv(i-1)]
            ffront = frequency[perm.sigmaInv(i)]
            if (ffront < fback):
                admissible.append((i-1, i))

        return admissible





    @staticmethod
    def test():
        def phi(perm):
            #let 3 ~ s, 4 ~ r

            sIndex = perm.sigma(3)#3 is innate index, sIndex is order index

            temp = []
            for i in range(0,3): #i is innate index, sigma takes innate to order
                if perm.sigma(i) < perm.sigma(4): #case: not in R
                    temp.append(1)
                else: #case in R
                    temp.append(1-sIndex * (1.0/10.0))
            for i in range(3,5): #parameters
                temp.append(0)
            return temp
        permutation1 = [1,3,2,4,0]
        p1 = Permutation(permutation1)

        system = System(5, phi)
        print "sheep live here"
        print system.admissibleTranspositions(p1)

    @staticmethod
    def makeZeros(n):
        temp = []
        for i in range(0,n):
            temp.append(0.0)
        return temp

    @staticmethod
    def makeSeparationConstraint(epsilon):
        #for now this is NOT agnostic to the cell cycle model.
        #we should only separate the parameters.  Otherwise,
        #nothting will ever happen
        #A1 = [[0,0,0,-1,0],[0,0,0,0,1],[0,0,0,1,-1]]
        #b1 = [-1 * epsilon, 1 - epsilon, -1 * epsilon]

        #monday monday monday, nathan adds a specific value constraint to r and s to narrow shit down
        A1 = [[0,0,0,-1,0],[0,0,0,0,1],[0,0,0,1,-1],[0,0,0,1,0],[0,0,0,0,1]]
        b1 = [-1 * epsilon, 1 - epsilon, -1 * epsilon, 0.2, 0.8]
        constraint = ConvexSet(A1, b1)

        return constraint

    @staticmethod
    def testConcat():
        def phi(perm):
            #let 3 ~ s, 4 ~ r

            sIndex = perm.sigma(3)#3 is innate index, sIndex is order index

            temp = []
            for i in range(0,3): #i is innate index, sigma takes innate to order
                if perm.sigma(i) < perm.sigma(4): #case: not in R
                    temp.append(1)
                else: #case in R
                    temp.append(1-sIndex * (1.0/10.0))
            for i in range(3,5): #parameters
                temp.append(0)
            return temp
        permutation1 = [1,3,2,4,0]
        p1 = Permutation(permutation1)
        trans = (2,3)
        system = System(5, phi)
        w1 = system.word(p1)
        w2 = system.concat(w1, trans)
        print "word 1: Set"
        print w1.set.A
        print w1.set.b
        print "word 2: Set"
        print w2.set.A
        print w2.set.b
        print "word 1: Map"
        print w1.map.A
        print w1.map.b
        print "word 2: Map"
        print w2.map.A
        print w2.map.b




System.testConcat()
#System.test()






