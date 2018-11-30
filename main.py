from ClassObj import TAMUClass
from ClassManipulator import Classer
from ConfigReader import ConfigReader
import time


# TODO: Logged out checker
# TODO: Ability to 'time snipe' - tell it your registration time and it will snipe classes down to the millisecond.

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
        crns, courses = classBrowser.getData(classItem.subjectAbbr, classItem.courseNumber)        
        classItem.setSectionNums(courses)
        classItem.setCRNs(crns)
    else:
        crns, crsNums = classBrowser.getData(classItem.subjectAbbr, classItem.courseNumber, classItem.sectionNumbers)
        classItem.setSectionNums(crsNums)   # Might have been reordered
        classItem.setCRNs(crns)

print("INITIALIZED!")
    


runs = 0

# Objs are now setup and stuff.
# TODO: Add caching so that this step only has to be run when ini file is changed.

# This is the big while loop daddy
# All it does is:
#                   1.) Check for open spots for all classes and stuff
#                   2.) Updates the variables of the classes
#                   3.) Checks to see if any of the classes specified has an open spot.
while(len(classes) > 0):

    for classItem in classes:
        print("Checking: " + classItem.subjectAbbr, classItem.courseNumber)

        spots = classBrowser.checkSpots(classItem.subjectAbbr, classItem.courseNumber, classItem.sectionNumbers)
        classItem.updateRemainingSpots(spots)
        message = classItem.checkOpenSpotMessage()

        # If theres an open
        if not message == "":
            print(message)
            classBrowser.emailNotif(message, configs.emailTo, configs.emailFrom, configs.emailPass)
            
            toBeAdded = classItem.checkAutoAdd()
            # If the user wanted a class to be auto added
            if(classItem.addClass and len(toBeAdded) > 0):
                # Gets list of good CRNs
                
                tries = 0
                success = False

                # If theres a class that needs to be dropped.
                if(classItem.needDrop):
                    while(not success and tries < len(toBeAdded)):
                        # dropThenAddClass returns 0 if it was successful
                        success = classBrowser.dropThenAddClass(classItem.conflictCRN, toBeAdded[tries]) ==0
                        tries += 1
                else:
                    while(not success and tries < len(toBeAdded)):
                        # addClass returns 0 if it was successful
                        success = classBrowser.addClass(toBeAdded[tries]) ==0
                        tries += 1
                
                # just feedback for user
                if(success):
                    print("SUCCESS CONFIRMED BOIS")
                    classes.remove(classItem)
                    print("Class removed from further scans")
                else:
                    print("Failed. Will Keep scanning.")



    runs=runs+1
    print("Completed " + str(runs) + " scans!")

    # sleep configured in config.ini
    time.sleep(configs.pollingRate) 

print("Congratz, you got everything =))))))")