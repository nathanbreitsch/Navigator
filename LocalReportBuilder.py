from Navigator import Navigator
from ConvexSet import ConvexSet
from cvxSolver import cvxSolver
from System import System
import json

class LocalReportBuilder:
    def __init__(self, fileName):
        print("i am getting better at oo arch")
        navi = Navigator.readPickle(fileName)
        self.words = navi.wordsGenerated


    def makeFMapReport(self):

        dict = {}
        dict["regions"] = []

        crossSections = []
        for word in self.words:

            #if word.isFPrimitive():
            if len(word.sequence) == 4:

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


    def makePeriodicOrbitReport(self):
        for word in data:
            if word.testPeriodic():
                print("\nsequence: ")
                for trans in word.eventLog:
                    print trans
                    print("\t")





    @staticmethod
    def main():
        reportBuilder = LocalReportBuilder("wordsGenerated.p")
        reportBuilder.makeFMapReport()
        #reportBuilder.makePeriodicOrbitReport()
    @staticmethod
    def makeCrossSectionConstraints():
        A = [[1,0,0,0,0],[0,0,0,1,0],[0,0,0,0,1],[-1,0,0,0,0],[0,0,0,-1,0],[0,0,0,0,-1]]
        b = [0,.2,.8,0,-.2,-.8]
        constraint = ConvexSet(A, b)
        return constraint

LocalReportBuilder.main()
