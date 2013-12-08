from Navigator import Navigator
from ConvexSet import ConvexSet
from cvxSolver import cvxSolver
from System import System
import json

class LocalReportBuilder:
    def __init__(self, words):
        self.words = words

    def makeReport(self):

        dict = {}
        dict["regions"] = []

        crossSections = []
        for word in self.words:
            if word.isFPrimitive():
                #cross section computation

                #old logic
                #crossSectionConstraints = LocalReportBuilder.makeCrossSectionConstraints()
                #tempSet = ConvexSet.intersect(crossSectionConstraints, word.set)

                #new logic
                crossSection = word.set.standardCrossSection([0,'?','?',.4,.6])


                solution = cvxSolver.solve(crossSection)
                if solution["status"] == "optimal":
                    #somehow compute vertices of the set in 2d
                    #vertices = LocalReportBuilder.computeVertices(tempSet)
                    cxName = ""
                    for event in word.eventLog:
                        cxName += str(event)
                    cxName = cxName.replace(" ", "")
                    cxName = cxName.replace("/", "")
                    cxName = cxName.replace("[", "")
                    cxName = cxName.replace("]", "")
                    cxName = cxName.replace(",", "")
                    cxName = cxName.replace("'", "")


                    crossSection.writeIne(cxName, "./data/" + cxName + ".ine")
                    crossSection.writeVertices("./data/" + cxName + ".ver")
                    dict["regions"].append(crossSection.getDict())
                    print "vertices: "
                    print crossSection.getVertices()
                    temp = {}
                    temp["crossSection"] = crossSection
                    temp["eventLog"] = word.eventLog
                    temp["initialP"] = word.sequence[0].permutation
                    crossSections.append(temp)
        print ("Report on F map regions")
        print len(crossSections)
        for piece in crossSections:
            print piece["initialP"]
            print piece["eventLog"]

        f = open("./data/fMap.json", "w")
        f.write(json.dumps(dict))
        f.close()


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