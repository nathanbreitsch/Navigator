__author__ = 'NathanBreitsch'
from System import *

class Navigator:
    def __init__(self, system):
        self.system = system
        self.admissableTrannies = []
        for i in range(0, system.dim - 1):
            self.admissableTrannies.append([i, i+1])
        self.admissableTrannies.append("R")
        self.cutoff_length = 11

    def navigate(self):
        numDoorsChecked = 0
        numDoorsOpened = 0
        numValid = 0
        initialP = [0,1,3,2,4]
        p0 = Permutation(initialP)
        gen1 = []
        gen1.append(self.system.word(p0))
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
                        numDoorsOpened += 1
            generations.append(nextList)
        print "lengths:"
        for i in range(0,len(generations)):
            print "generation: " + str(i) + " ------ " + str(len(generations[i]))
        print "doors checked: " + str(numDoorsChecked)
        print "doors opened: " + str(numDoorsOpened)
        print "doors valid: " + str(numValid)
        for word in generations[9]:
            print word.toString()


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