from numpy import *
from cvxSolver import *
from Permutation import *
from pymongo import MongoClient

class Word:
    def __init__(self, sequence):
        #seqence of permutations
        self.sequence = sequence
        self.flips = []
        self.feasible = "unknown"
        self.set = []
        self.map = []
        self.eventLog = []

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

    def serialize(self):
        representation = {}
        #flips, feasible should already be ok
        #representation["sequence"] = self.sequence
        representation["flips"] = self.flips
        representation["feasible"] = self.feasible
        #need to do some serious serialization of the maps and permutations and shit
        sequenceJson = []
        for p in self.sequence:
            sequenceJson.append(p.serialize())
        representation["sequence"] = sequenceJson
        #map
        representation["map"] = self.map.serialize()
        #set
        representation["set"] = self.set.serialize()
        return representation

    def deserialize(self, representation):
        newObject = Word(representation["sequence"])
        newObject.flips = representation["flips"]
        newObject.feasible = representation["feasible"]
        newObject.map = AffineMap(representation["map"]["A"], representation["set"]["b"])
        newObject.set = matrix(representation["set"]["A"],representation["set"]["b"])

    def isFPrimitive(self):
        #only F map
        if self.flips[-1] != "R":
            return False
        #no double F
        for i in range(0, len(self.flips) - 1):
            if self.flips[i] == "R":
                return False
        return True


    #upload relevant data about the word to the cloud
    def sendToCloud(self):
        #client = MongoClient('localhost', 28017)
        client = MongoClient()
        db = client.Hilbert
        wordCollection = db.words
        representation = self.serialize()
        wordCollection.insert(representation)









