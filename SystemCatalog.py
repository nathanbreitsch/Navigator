__author__ = 'NathanBreitsch'
from System import System

#defines a list of Systems


def phi(perm):
    #let 3 ~ s, 4 ~ r
    sIndex = perm.sigma(3)
    temp = []
    for i in range(0,3):
        if perm.sigma(i) < perm.sigma(4): #case: not in R
            temp.append(1)
        else: #case in R
            temp.append(1-sIndex * (1.0/10.0))
    for i in range(3,5): #parameters
        temp.append(0)
    return temp
system0 = System(5, phi)

systemList = []
systemList.append(system0)

