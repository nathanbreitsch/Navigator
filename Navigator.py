__author__ = 'NathanBreitsch'
from System import *

class Navigator:
    def __init__(self, system):
        self.system = system

    def doThatThingYouDo(self):
        initialP = [3,1,2,0,4]
        p0 = Permutation(initialP)



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
        navi.doThatThingYouDo()

Navigator.test()