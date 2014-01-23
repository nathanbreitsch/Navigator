__author__ = 'NathanBreitsch'

from ConvexSet import ConvexSet

class ConvexGeometry:
    @staticmethod
    def preImage(map,set):
        tempA = set.A * map.A
        tempb = set.b - set.A * map.b
        return ConvexSet(tempA, tempb)

    @staticmethod
    def test():
        print "ys"
