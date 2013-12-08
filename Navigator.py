__author__ = 'NathanBreitsch'
from System import *
#from ConvexSet import ConvexSet
import random
import numpy


class Navigator:
    def __init__(self, system):
        self.system = system
        self.admissableTrannies = []
        for i in range(0, system.dim - 1):
            self.admissableTrannies.append([i, i+1])
        self.admissableTrannies.append("R")
        self.cutoff_length = 10
        self.wordsGenerated = []

    def navigate(self):
        numDoorsChecked = 0
        numDoorsOpened = 0
        numValid = 0
        #initialP = [0,1,3,2,4]
        #p00 = Permutation(initialP)

        #generate representatives of each symmetry class
        gen1 = []
        for i in range(1,4):
            for j in range(i+1,5):
                temp = [0,3,4]
                temp.insert(i,1)
                temp.insert(j,2)
                gen1.append(self.system.word(Permutation(temp)))
        #gen1.append(self.system.word(p00))
        generations = []
        generations.append(gen1)
        for currentLength in range(2, self.cutoff_length):
            currentList = generations[len(generations)-1]
            nextList = []
            for word in currentList:
                for transposition in self.admissableTrannies:
                    candidateWord = self.system.concat(word, self.system.word(word.lastInSequence().transpose(transposition)), transposition)
                    numDoorsChecked += 1
                    if candidateWord.set != []:
                        numValid += 1
                    if candidateWord.testFeasibility():
                        nextList.append(candidateWord)
                        self.wordsGenerated.append(candidateWord)
                        numDoorsOpened += 1
            generations.append(nextList)
        print "lengths:"
        for i in range(0,len(generations)):
            print "generation: " + str(i) + " ------ " + str(len(generations[i]))
        print "doors checked: " + str(numDoorsChecked)
        print "doors opened: " + str(numDoorsOpened)
        print "doors valid: " + str(numValid)
        for word in generations[4]:
            print word.toString()

        #look for periodic orbits
        total  = 0
        orbits = []
        for list in generations:
            for word in list:
                #word.sendToCloud()
                total += 1
                if self.testStrictPeriodic(word):
                   orbits.append(word)
        print "# periodic orbit"
        print len(orbits)
        print "out of"
        print total

    def testStrictPeriodic(self, word):
        #first decide whether the transpositions compose to identity
        netTrans = word.netTransposition()
        if not netTrans.isIdentity():
            return False
        #next, obtain the full poincare map
        Fmap = word.map
        #construct the set of constraints for fixed point
        A1 = add(Fmap.A, -1.0 * AffineMap.identity(self.system.dim).A)
        A2 = add(AffineMap.identity(self.system.dim).A, -1 * Fmap.A)
        b2 = Fmap.b
        b1 = -1.0 * b2
        A = concatenate((A1, A2))
        b = concatenate((b1, b2))
        cs = ConvexSet(A, b)
        FixedPoints = cs.intersect(cs, word.set())
        #test feasibility
        solution = cvxSolver.solve(FixedPoints)
        return (solution['status']=='optimal')

    def testPeriodic(self, word):
        #first decide whether the transpositions compose to an element of G
        netTrans = word.netTransposition()
        if not self.system.invariant(netTrans):
            return False
        #next compose the time map with the preserving permutation
        Fmap = AffineMap.compose(netTrans.mapRepresentation(), word.map)
        #construct the set of constraints for fixed point
        A1 = add(Fmap.A, -1.0 * AffineMap.identity(self.system.dim).A)
        A2 = add(AffineMap.identity(self.system.dim).A, -1 * Fmap.A)
        b2 = Fmap.b
        b1 = -1.0 * b2
        A = concatenate((A1,A2))
        b = concatenate((b1,b2))
        cs = ConvexSet(A,b)
        FixedPoints = cs.intersect(cs, word.set())
        #test feasibility
        solution = cvxSolver.solve(FixedPoints)
        return (solution['status']=='optimal')

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
        system = System(5, phi)
        navi = Navigator(system)
        navi.navigate()

Navigator.test()