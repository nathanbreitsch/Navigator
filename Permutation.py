import copy

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

    def sigma(self, index):
        return(self.permutation[index])

    def sigmaInv(self,index):
        for i in range(0, self.dim()):
            if self.permutation[i] == index:
                return i
        return -1

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


Permutation.test()