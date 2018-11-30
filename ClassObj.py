

class TAMUClass:

    def __init__(self, subj, courseNumber, sectionNumbers, conflictClass=None, addSections=None, **kwargs):
        if not conflictClass == None:
            self.needDrop = True
            self.conflictCRN = conflictClass
        else:
            self.needDrop = False

        if not addSections == None:
            self.addClass = True
            self.specialSections = addSections
        else:
            self.addClass = False

        self.subjectAbbr = subj
        self.courseNumber = courseNumber
        self.sectionNumbers = sectionNumbers
    
    
    def setSectionNums(self, secNums):
        self.sectionNumbers = secNums

    def setCRNs(self, crns):
        self.crns = crns
        self.sec2crn = dict(zip(self.sectionNumbers, self.crns))
        self.crn2sec = dict(zip(self.crns, self.sectionNumbers))

    def setRemainingSpots(self, remainingSpots):
        self.remainingSpots = remainingSpots

    def checkOpen(self):
        self.indicesOpen = []

        for x in range(len(self.remainingSpots)):
            if self.remainingSpots[x] > 0:
                self.indicesOpen.append(x)

    def checkOpenSpotMessage(self): 
        self.checkOpen()

        out = ""       
        if(len(self.indicesOpen) == 0):
            return out
        else:
            out = "The following classes are open for " + self.subjectAbbr + " " + self.courseNumber + "\n"
            for i in self.indicesOpen:
                out += "Section " + self.sectionNumbers[i] + "\t CRN " + self.crns[i] + "\n"
            return out



    """
    Checks to see if any courses will be auto-added.
    Returns an array with all courses to be auto-aded.
    """
    def checkAutoAdd(self):
        self.checkOpen()
        goodCRNs = []

        for i in self.indicesOpen:
            if self.sectionNumbers[i] in self.specialSections:
                goodCRNs.append(self.sec2crn[self.sectionNumbers[i]])

        return goodCRNs


