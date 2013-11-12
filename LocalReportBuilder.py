from Navigator import Navigator
from ConvexSet import ConvexSet
from cvxSolver import cvxSolver
from System import System

class LocalReportBuilder:
    def __init__(self, words):
        self.words = words

    def makeReport(self):
        crossSections = []
        for word in self.words:
            if word.isFPrimitive():
                #cross section computation
                crossSectionConstraints = LocalReportBuilder.makeCrossSectionConstraints()
                tempSet = ConvexSet.intersect(crossSectionConstraints, word.set)
                solution = cvxSolver.solve(tempSet)
                if solution["status"] == "optimal":
                    #somehow compute vertices of the set in 2d
                    #vertices = LocalReportBuilder.computeVertices(tempSet)
                    temp = {}
                    temp["tempSet"] = tempSet
                    temp["eventLog"] = word.eventLog
                    temp["initialP"] = word.sequence[0].permutation
                    crossSections.append(temp)
        print ("Report on F map regions")
        print len(crossSections)
        for piece in crossSections:
            print piece["initialP "]
            print piece["eventLog"]

    @staticmethod
    def main():
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
        reportBuilder = LocalReportBuilder(navi.wordsGenerated)
        reportBuilder.makeReport()

    @staticmethod
    def makeCrossSectionConstraints():
        A = [[1,0,0,0,0],[0,0,0,1,0],[0,0,0,0,1],[-1,0,0,0,0],[0,0,0,-1,0],[0,0,0,0,-1]]
        b = [0,.2,.8,0,-.2,-.8]
        constraint = ConvexSet(A, b)
        return constraint

LocalReportBuilder.main()