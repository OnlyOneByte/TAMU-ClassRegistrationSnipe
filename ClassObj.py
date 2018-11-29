

class TAMUClass:

    def __init__(self, subj, courseNumber, sectionNumbers):
        self.subjectAbbr = subj
        self.courseNumber = courseNumber
        self.sectionNumbers = sectionNumbers
    
    def sectionToCRN(self, sectionNumber):
        try:
            return self.sec2crn[sectionNumber]
        except:
            print("CRNS NOT YET DEFINED.")

    def setSectionNums(self, secNums):
        self.sectionNumbers = secNums

    def setCRNs(self, crns):
        self.crns = crns
        self.sec2crn = dict(zip(self.sectionNumbers, self.crns))
        self.crn2sec = dict(zip(self.crns, self.sectionNumbers))

    def setRemainingSpots(self, remainingSpots):
        self.remainingSpots = remainingSpots

    def checkOpenSpots(self):
        indicesOpen = []
        out = ""

        for x in range(len(self.remainingSpots)):
            if self.remainingSpots[x] > 0:
                indicesOpen.append(x)

        
        if(len(indicesOpen) == 0):
            return out
        else:
            out = "The following classes are open for " + self.subjectAbbr + " " + self.courseNumber + "\n"
            for i in indicesOpen:
                out += "Section " + self.sectionNumbers[i] + "\t CRN " + self.crns[i] + "\n"
            return out

