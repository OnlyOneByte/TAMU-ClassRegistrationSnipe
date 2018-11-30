from ClassObj import TAMUClass
from ClassManipulator import Classer
from ConfigReader import ConfigReader
import time

# Opens configuration file
configs = ConfigReader("config.ini")
# Make sure to change this to whatever your cofig file is


# Opens the browser
classBrowser = Classer(configs.user, configs.password)

# Gets classes from the config reader
classes = configs.classes

# Initialization step.
for classItem in classes:
    print("Initializing: " + classItem.subjectAbbr, classItem.courseNumber)
    # Initializing CRNs
    if(classItem.sectionNumbers[0] == "ALL"):
        crns, courses, openSpots = classBrowser.getData(classItem.subjectAbbr, classItem.courseNumber)        
        classItem.setSectionNums(courses)
        classItem.setCRNs(crns)
        classItem.setRemainingSpots(openSpots)
    else:
        crns, crsNums, openSpots = classBrowser.getData(classItem.subjectAbbr, classItem.courseNumber, classItem.sectionNumbers)
        classItem.setSectionNums(crsNums)   # Might have been reordered
        classItem.setCRNs(crns)
        classItem.setRemainingSpots(openSpots)

print("INITIALIZED!")
    


runs = 0

# Objs are now setup and stuff.
# TODO: Add caching so that this step only has to be run when ini file is changed.

# This is the big while loop daddy
# All it does is:
#                   1.) Check for open spots for all classes and stuff
#                   2.) Updates the variables of the classes
#                   3.) Checks to see if any of the classes specified has an open spot.
while(True):

    for classItem in classes:
        print("Checking: " + classItem.subjectAbbr, classItem.courseNumber)

        spots = classBrowser.checkSpots(classItem.subjectAbbr, classItem.courseNumber, classItem.sectionNumbers)
        classItem.setRemainingSpots(spots)
        message = classItem.checkOpenSpotMessage()
        if not message == "":
            print(message)
            classBrowser.emailNotif(message, configs.emailTo, configs.emailFrom, configs.emailPass)


    runs=runs+1
    print("Completed " + str(runs) + " runs!")
    # sleep configured in config.ini
    time.sleep(configs.pollingRate) 