from numpy import *
from cvxSolver import *
from Permutation import *
from pymongo import MongoClient
from AffineMap import AffineMap
from ConvexSet import ConvexSet

class Word:
    def __init__(self, sequence):
        #seqence of permutations
        #todo fix this bad practice of setting things to [] initially
        #todo: figure out how to do code completion in for instance variables
        self.sequence = sequence
        self.flips = []
        self.feasible = "unknown"
        self.set = "unspecified"
        self.map = "unspecified"
        self.eventLog = []

    def eventLogString(self):
        logString = ""
        for event in self.eventLog:
            logString += str(event)
        return logString

    def dim(self):
        if self.sequence == []:
            return 0
        else:
            return self.sequence[0].dim()

    def toString(self):
        rtrn = ""
        for p in self.flips:
            rtrn += str(p)
        return rtrn

    def testFeasibility(self):
        if self.set == []:
            return False
        else:
            result = cvxSolver.solve(self.set)
            if (result['status'] == 'unknown'):
                f = open("log", "a")
                f.write(self.toString() + "\n")
                f.close()
            return (result['status']=='optimal')

    def testPrint(self):
        print "constraint A"
        print self.set.A
        print "constraint b"
        print self.set.b
        print "map A"
        print self.map.A

    def netTransposition(self):
        initial = self.sequence[0]
        inverse = initial.inverse()
        e = Permutation.identity(self.dim())
        for flip in self.flips:
            e = e.transpose(flip)
        e = Permutation.compose(initial, Permutation.compose(e, inverse))
        return e

    def lastInSequence(self):
        return self.sequence[len(self.sequence)-1]

    #returns dictionary representing the word object
    def serialize(self):
        representation = {}
        #flips, feasible should already be ok
        #representation["sequence"] = self.sequence
        representation["flips"] = self.flips
        representation["feasible"] = self.feasible
        #need to do serialization of the maps and permutations
        sequenceList = []
        for p in self.sequence:
            sequenceList.append(p.serialize())
        representation["sequence"] = sequenceList
        #map
        representation["map"] = self.map.serialize()
        #set
        representation["set"] = self.set.serialize()
        return representation

    #given dictionary representation of word object, returns word object
    @staticmethod
    def deserialize(representation):
        sequence = []
        for p in representation["sequence"]:
            sequence.append(Permutation.deserialize(p))
        newWord = Word(sequence)
        newWord.flips = representation["flips"]
        newWord.feasible = representation["feasible"]
        newWord.map = AffineMap.deserialize(representation["map"])
        newWord.set = ConvexSet.deserialize(representation["set"])
        return newWord
        #newObject.map = AffineMap(representation["map"]["A"], representation["set"]["b"])
        #newObject.set = matrix(representation["set"]["A"],representation["set"]["b"])

    #returns true iff the block word represents a single F map (single rotation event)
    def isFPrimitive(self):
        #only F map
        if self.flips[-1] != "R":
            return False
        #no double F
        for i in range(0, len(self.flips) - 1):
            if self.flips[i] == "R":
                return False
        return True

    def testPeriodic(self):
        #first decide whether the transpositions compose to an element of G
        netTrans = self.netTransposition()
        if not self.system.invariant(netTrans):
            return False
        #next compose the time map with the preserving permutation
        Fmap = AffineMap.compose(netTrans.mapRepresentation(), self.map)
        #construct the set of constraints for fixed point
        A1 = add(Fmap.A, -1.0 * AffineMap.identity(self.system.dim).A)
        A2 = add(AffineMap.identity(self.system.dim).A, -1 * Fmap.A)
        b2 = Fmap.b
        b1 = -1.0 * b2
        A = concatenate((A1,A2))
        b = concatenate((b1,b2))
        cs = ConvexSet(A,b)
        FixedPoints = cs.intersect(cs, self.set())
        #test feasibility
        solution = cvxSolver.solve(FixedPoints)
        return (solution['status']=='optimal')

    #def writeToIneFile(self, filename):
    #    name = self.eventLogString()
    #    contents = self.set.ineRepresentation()
    #    f = open(filename, "w")
    #    f.write(name + "\n" + contents)
    #    f.close()


    #upload relevant data about the word to the cloud
    def sendToCloud(self):
        #client = MongoClient('localhost', 28017)
        client = MongoClient()
        db = client.Hilbert
        wordCollection = db.words
        representation = self.serialize()
        wordCollection.insert(representation)












