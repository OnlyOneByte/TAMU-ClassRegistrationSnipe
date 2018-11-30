

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
        self.remainingSpots = []
    
    
    def setSectionNums(self, secNums):
        self.sectionNumbers = secNums

    def setCRNs(self, crns):
        self.crns = crns
        self.sec2crn = dict(zip(self.sectionNumbers, self.crns))
        self.crn2sec = dict(zip(self.crns, self.sectionNumbers))
    
    def setRemainingSpots(self, remainingSpots):
        self.remainingSpots = remainingSpots

    # Shuffles it around.
    def updateRemainingSpots(self, remainingSpots):
        self.oldSpots = self.remainingSpots
        self.remainingSpots = remainingSpots

    def checkOpen(self, spots):
        indicesOpen = []

        for x in range(len(spots)):
            if spots[x] > 0:
                indicesOpen.append(x)

        return indicesOpen

    def checkOpenSpotMessage(self): 
        openIndex = self.checkOpen(self.remainingSpots)

        out = ""       
        if(len(openIndex) == 0):
            return out
        else:
            out = "The following classes are open for " + self.subjectAbbr + " " + self.courseNumber + "\n"
            for i in openIndex:
                out += "Section " + self.sectionNumbers[i] + "\t CRN " + self.crns[i] + "\n"
            return out



    """
    Checks to see if any courses will be auto-added.
    Returns an array with all courses to be auto-aded.
    - Only returns if it was open for 2 consecutive scans
    """
    def checkAutoAdd(self):
        openCurrent = self.checkOpen(self.remainingSpots)
        openLast = self.checkOpen(self.oldSpots)
        goodCRNs = []

        for i in openCurrent:
            if self.sectionNumbers[i] in self.specialSections and i in openLast:
                goodCRNs.append(self.sec2crn[self.sectionNumbers[i]])

        return goodCRNs


