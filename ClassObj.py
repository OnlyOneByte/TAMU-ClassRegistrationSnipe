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
    

    """
    set the section numbers to be the list passed in.

    args
        secNums: list<string> of all the section numbers

    no return
    """
    def setSectionNums(self, secNums):
        self.sectionNumbers = secNums

    """
    Sets the CRNs and updates all the dictionaries

    args
        crns: list<string> of all the crns

    no return
    """
    def setCRNs(self, crns):
        self.crns = crns
        self.sec2crn = dict(zip(self.sectionNumbers, self.crns))
        self.crn2sec = dict(zip(self.crns, self.sectionNumbers))
    
    """
    Updates the remaining spots array to new scan values. Keeps a history of 1 scan.

    args
        remainingSpots: Array<int> of open spots.

    no return
    """
    def updateRemainingSpots(self, remainingSpots):
        self.oldSpots = self.remainingSpots
        self.remainingSpots = remainingSpots


    """
    Returns any indices of values greater than 0 in the array

    args
        spots: list<ints> to be checked

    return type: list of ints
    """
    def checkOpen(self, spots):
        indicesOpen = []

        for x in range(len(spots)):
            if spots[x] > 0:
                indicesOpen.append(x)

        return indicesOpen


    """
    REturns an email message detailing any classes that are open, and if
    any classes will be auto added.

    return type: string
    """
    def checkOpenSpotMessage(self): 
        openIndex = self.checkOpen(self.remainingSpots)

        out = ""  

        # Just any class that is open     
        if(len(openIndex) == 0):
            return out
        else:
            out = "The following classes are open for " + self.subjectAbbr + " " + self.courseNumber + "\n"
            for i in openIndex:
                out += "Section " + self.sectionNumbers[i] + "\t CRN " + self.crns[i] + "\n"
        

        # Auto add. Tells you if a section is about to be auto-added
        autoAdd = self.checkAutoAdd()
        if(len(autoAdd) == 0):
            return out
        else:
            out += "\nThe following classes (attempt) to be auto-registered:"
            for crn in autoAdd:
                out += "Section " + self.crn2sec[crn] + "\t CRN " + crn + "\n"

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


        if self.needDrop:
            for i in openCurrent:
                if self.sectionNumbers[i] in self.specialSections and i in openLast:
                    goodCRNs.append(self.sec2crn[self.sectionNumbers[i]])
        else:
            for i in openCurrent:
                if self.sectionNumbers[i]:
                    goodCRNs.append(self.sec2crn[self.sectionNumbers[i]])

        return goodCRNs


