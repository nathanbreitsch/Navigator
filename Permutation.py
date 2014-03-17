from copy import deepcopy
from AffineMap import *


class Permutation:
    def __init__(self, perm):
        self.permutation = perm


    #return list of adjacent permutations
    def getAdjacent(self):
        adjacentList = []
        for i in range(0, self.dim-1):
            for j in range(i+1, self.dim):
                nextPerm = list(self.permutation)
                temp = nextPerm[i]
                nextPerm[i] = nextPerm[j]
                nextPerm[j] = temp
                adjacentList.append(Permutation(nextPerm))

    def dim(self):
        return len(self.permutation)

    #what goes to position index under the permutation?
    #converts order into innate
    def sigmaInv(self, index):
        return(self.permutation[index])

    #where does index go under the permutation
    #converts innate into order
    def sigma(self,index):
        for i in range(0, self.dim()):
            if self.permutation[i] == index:
                return i
        return -1

    def inverse(self):
        temp = []
        for i in range(0, self.dim()):
            temp.append(self.sigmaInv(i))
        return Permutation(temp)


    #construct identity permutation
    @staticmethod
    def identity(dim):
        temp = []
        for i in range(0, dim):
            temp.append(i)
        return Permutation(temp)

    #compose symbols (they need to be same length)
    @staticmethod
    def compose(perm1, perm2):
        p1 = perm1.permutation
        p2 = perm2.permutation
        temp = []
        for i in range(0, len(p1)):
            temp.append(p1[p2[i]])
        return Permutation(temp)

    #return transposition of permutation
    def transpose(self, transposition):
        newPerm = deepcopy(self.permutation)
        if transposition == "R":
            temp = newPerm[len(newPerm)-1]
            for i in range(1, len(newPerm)):
                newPerm[len(newPerm) - i] = newPerm[len(newPerm)-i-1]
            newPerm[0] = temp
        else:
            a = transposition[0]
            b = transposition[1]
            temp = newPerm[a]
            newPerm[a] = newPerm[b]
            newPerm[b] = temp
        return Permutation(newPerm)

    #return AffineMap representation of permutation
    def mapRepresentation(self):
        b = Permutation.makeZeros(self.dim())
        A = []
        for i in range(0, self.dim()):
            nextRow = []
            for j in range(0, self.dim()):
                if j == self.sigma(i):
                    nextRow.append(1)
                else:
                    nextRow.append(0)
            A.append(nextRow)
        return AffineMap(A, b)

    def serialize(self):
        return self.permutation


    def isIdentity(self):
        for i in range(1, self.dim()):
            if self.permutation[i] != self.permutation[i-1] + 1:
                return False
        return True

    #construct swap permuation of given dimension
    @staticmethod
    def swap(dim, n1, n2):
        swapper = Permutation.identity(dim)
        temp = swapper.permutation[n1]
        swapper.permutation[n1] = swapper.permutation[n2]
        swapper.permutation[n2] = temp
        return swapper

    @staticmethod
    def test():
        swap1 = Permutation.swap(5,2,3)
        swap2 = Permutation.swap(5,4,1)
        swap3 = Permutation.compose(swap1, swap2)
        print swap1.permutation
        print swap2.permutation
        print swap3.permutation

    @staticmethod
    def makeZeros(n):
        temp = []
        for i in range(0,n):
            temp.append(0.0)
        return temp


Permutation.test()