from Navigator import Navigator
from ConvexSet import ConvexSet
from cvxSolver import cvxSolver
from System import System
import json

class LocalReportBuilder:
    def __init__(self):
        print("i am bad at oo arch")

    def makeReport(self):
        def phi(perm):
            #let 3 ~ s, 4 ~ r

            sIndex = perm.sigmaInv(3)

            temp = []
            for i in range(0,3):
                if perm.sigmaInv(i) < perm.sigmaInv(4): #case: not in R
                    temp.append(1)
                else: #case in R
                    temp.append(1-sIndex * (0.0/10.0))
            for i in range(3,5): #parameters
                temp.append(0)
            return temp
        system = System(5, phi)
        navi = Navigator(system)
        navi.navigate()
        self.words = navi.wordsGenerated

        dict = {}
        dict["regions"] = []

        crossSections = []
        for word in self.words:

            #if len(word.flips) == 6:
            #if navi.testPeriodic(word):
            if word.isFPrimitive():
                #print word.flips
                #cross section computation

                #old logic
                #crossSectionConstraints = LocalReportBuilder.makeCrossSectionConstraints()
                #tempSet = ConvexSet.intersect(crossSectionConstraints, word.set)

                #new logic
                crossSection = word.set.standardCrossSection([0,'?','?',.4,.6])
                #crossSection = word.set.standardCrossSection([0,0.25,0.75,'?','?'])

                solution = cvxSolver.solve(crossSection)
                if solution["status"] == "optimal":
                    #somehow compute vertices of the set in 2d
                    #vertices = LocalReportBuilder.computeVertices(tempSet)
                    cxName = ""
                    for event in word.flips:
                        cxName += str(event)
                    cxName = cxName.replace(" ", "")
                    cxName = cxName.replace("/", "")
                    cxName = cxName.replace("[", "")
                    cxName = cxName.replace("]", "")
                    cxName = cxName.replace(",", "")
                    cxName = cxName.replace("'", "")


                    #crossSection.writeIne(cxName, "./data/" + cxName + ".ine")
                    #crossSection.writeVertices("./data/" + cxName + ".ver")
                    dict["regions"].append(crossSection.getDict(cxName))
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

        f = open("data/fMap.js", "w")
        f.write("jsonObject = ")
        f.write(json.dumps(dict))
        f.close()


    @staticmethod
    def main():
        reportBuilder = LocalReportBuilder()
        reportBuilder.makeReport()

    @staticmethod
    def makeCrossSectionConstraints():
        A = [[1,0,0,0,0],[0,0,0,1,0],[0,0,0,0,1],[-1,0,0,0,0],[0,0,0,-1,0],[0,0,0,0,-1]]
        b = [0,.2,.8,0,-.2,-.8]
        constraint = ConvexSet(A, b)
        return constraint

LocalReportBuilder.main()