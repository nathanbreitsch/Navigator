from numpy import *
import Word
import Permutation as perm

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
        for i in range(0, symbol.dim()):
            newRow = zeros(symbol.dim())
            newRow[]


        return temp


    def concat(self, w1, w2):
        temp = Word()
        temp.sequence = []
        temp.sequence.extend(w1.sequence)
        temp.sequence.extend(w2.sequence)
        temp.flips.extend(w1.flips)
        #todo: append middle flip
        temp.flips.extend(w2.flips)

        #todo: compute constraints and map

        return temp


    @staticmethod
    def test():
        print "testing testing 123"
        def phi(perm):
            permutation = perm.permutation
            #let 3 ~ s, 4 ~ r
            rIndex = 0
            sIndex = 0
            while(permutation[rIndex] != 4):
                rIndex += 1
            while(permutation[sIndex] != 3):
                sIndex += 1
            temp = []
            for i in range(0, 5):
                if i == rIndex or i == sIndex:
                     temp.append(0)
                elif i < rIndex:
                    temp.append(1)
                else:
                    temp.append(1 - sIndex * (1.0/10.0))
            return temp
        permutation = [1,2,4,0,3]
        p1 = perm.Permutation(permutation)
        print phi(p1)



        system = System(5, phi)


System.test()





