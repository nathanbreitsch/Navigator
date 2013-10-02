__author__ = 'NathanBreitsch'
from AffineMap import *
from ConvexSet import *

class ConvexGeometry:
    @staticmethod
    def preImage(map,set):
        tempA = set.A * map.A
        tempb = set.b - set.A * map.b
        return ConvexSet(tempA,tempb)

    @staticmethod
    def test():
        print "suck it!"
