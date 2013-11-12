from pymongo import MongoClient

class ReportBuilder():
    def __init__(self):
        client = MongoClient()
        db = client.Hilbert
        self.words = db.words

    def FmapCrossSectionReport(self):
        print self.words.count()


    @staticmethod
    def butidReport():
        reportBuilder = ReportBuilder()
        reportBuilder.FmapCrossSectionReport()




ReportBuilder.butidReport()
