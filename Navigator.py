__author__ = 'NathanBreitsch'
from System import System
from ConvexSet import ConvexSet
from Permutation import Permutation
from AffineMap import AffineMap
from numpy import add, concatenate
from cvxSolver import cvxSolver
import pickle
import SystemCatalog
from Word import Word
import pymongo
import random
import numpy



class Navigator:
    def __init__(self, systemId):
        self.system = SystemCatalog.systemList[systemId]
        self.systemId = systemId
        self.wordsGenerated = []
        self.length = 0
        self.cutoff_length = 8

    def makeSymbols(self):
        #generate representatives of each symmetry class (currently not gen purpose)
        self.wordsGenerated = []
        gen1 = []
        for i in range(1,4):
            for j in range(i+1, 5):
                temp = [0,3,4]
                temp.insert(i,1)
                temp.insert(j,2)
                self.wordsGenerated.append(self.system.word(Permutation(temp)))
        self.length = 1

    def navigate(self):
        self.wordsGenerated = []
        #generate representatives of each symmetry class (currently not gen purpose)
        gen1 = []
        for i in range(1,4):
            for j in range(i+1, 5):
                temp = [0,3,4]
                temp.insert(i,1)
                temp.insert(j,2)
                gen1.append(self.system.word(Permutation(temp)))
        generations = []
        generations.append(gen1)
        for currentLength in range(2, self.cutoff_length):
            currentList = generations[-1]
            nextList = []
            for word in currentList:
                for transposition in self.system.admissibleTranspositions(word.lastInSequence()):
                    candidateWord = self.system.concat(word,  transposition)
                    if candidateWord.testFeasibility():
                        nextList.append(candidateWord)
                        self.wordsGenerated.append(candidateWord)
            generations.append(nextList)
        self.length = self.cutoff_length;

    #calculates extensions of all sequences with given length
    def iterate(self):
        for word in self.wordsGenerated:
            if len(word.sequence) == self.length:
                for transposition in self.system.admissibleTranspositions(word.lastInSequence()):
                    candidateWord = self.system.concat(word,  transposition)
                    if candidateWord.testFeasibility():
                        self.wordsGenerated.append(candidateWord)
        self.length += 1

    #reads words from pickle file into
    def writePickle(self):
        pickle.dump(self.serialize(), open("./Pickle/wordsGenerated.p", "wb"))

    @staticmethod
    def readPickle(fileName):
        rep = pickle.load(open("./Pickle/" + str(fileName), "rb"))
        return Navigator.deserialize(rep)

    #returns dictionary representation of the object
    def serialize(self):
        rep = {}
        rep["systemId"] = self.systemId
        wordReps = []
        for word in self.wordsGenerated:
            wordReps.append(word.serialize())
        rep["wordsGenerated"] = wordReps
        rep["length"] = self.length
        rep["cutoff_length"] = self.cutoff_length
        return rep

    @staticmethod
    #return object given dictionary representation
    def deserialize(rep):
        navi = Navigator(rep["systemId"])
        wordsGenerated = []
        for word in rep["wordsGenerated"]:
            wordsGenerated.append(Word.deserialize(word))
        navi.wordsGenerated = wordsGenerated
        navi.length = rep["length"]
        navi.cutoff_length = rep["cutoff_length"]
        return navi



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

    #def makeDB(self, name):


    @staticmethod
    def test():
        navi = Navigator(0)
        navi.makeSymbols()
        for i in range(0, 7):
            navi.iterate()
        navi.writePickle()

    @staticmethod
    def SingleIteration():
        navi = Navigator.readPickle("wordsGenerated.p")
        navi.iterate()
        navi.writePickle()
#Navigator.test()

