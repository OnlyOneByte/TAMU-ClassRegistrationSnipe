from ClassObj import TAMUClass
from ClassManipulator import Classer
from ConfigReader import ConfigReader
import time
from datetime import datetime, timedelta
"""
This program has a safety feature if you intend to use this to replace classes rather than
snipe them. If you intend to replace a class with a better schedule one, then the program
will check to see if a spot is open for 2 consecutive scans before attempting to drop then add.
This is to prevent a false-positive from screwing with the system

- IF THE ADD FAILS, THE PROGRAM WILL RE-ADD THE OLD CLASS AGAIN.

The safety feature doesn't apply to straight additions because those you can do without risk.
"""

# TODO: Logged out checker
# TODO: Ability to 'time snipe' - tell it your registration time and it will snipe classes down to the millisecond.
# TODO: Add caching so that this step only has to be run when ini file is changed.
# TODO: Add ability to pause program
# TODO: Allow for variable registration terms


def checkClassRun(classItem):
    print("Checking: " + classItem.subjectAbbr, classItem.courseNumber)
    spots = classBrowser.checkSpots(classItem.subjectAbbr, classItem.courseNumber, classItem.sectionNumbers)
    classItem.updateRemainingSpots(spots)


def addClass(classItem):
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
            print("Successfully added class to your schedule!")
            classes.remove(classItem)
            print("Class removed from further scans")
        else:
            print("Failed. Will Keep scanning.")

"""
    This function is all about running continuously to check if someone changes classes around.
    This is to be run during registration time.
"""
def normalLoop():
    runs = 0
    startTotalT = time.time()

    # All it does is:
    #   1.) Check for open spots for all classes and stuff
    #   2.) Updates the variables of the classes
    #   3.) Checks to see if any of the classes specified has an open spot.
    #   4.) Attempts to register for classes indicated by user and are open.
    while(len(classes) > 0):
        startScanT = time.time()

        # Checks class item.
        for classItem in classes:
            checkClassRun(classItem)
            message = classItem.checkOpenSpotMessage()

            # If theres an open
            if not message == "":
                print(message)
                classBrowser.emailNotif(message, configs.emailTo, configs.emailFrom, configs.emailPass)
                addClass(classItem)
                

        # This is just informational stuff. Maybe to be used later.
        runs=runs+1
        deltaT = (time.time()-startTotalT)                              # Total time lapsed
        runTime = (time.time()-startScanT)                              # Time lapsed this run.
        avgTRun = (deltaT - (configs.pollingRate * (runs-1)))/runs      # average time per run. Removed sleep time.
        
        print("This run took", str(runTime), "seconds!")
        print("Average time per run:", str(avgTRun), "Total time open: " + str(deltaT))
        print("Completed " + str(runs) + " scans!")
        print("----------------------------------------------------------")

        # sleep configured in config.ini
        time.sleep(configs.pollingRate) 

def beforeOpenLoop():
    # Checks classes at 15, 10, and 5 minutes before open time.
    currTime = datetime.now()
    tdelta = configs.openTime - currTime
    print("Time until open: " + str(tdelta))

    # does a check.
    for classItem in classes:
        message = classItem.onlyOpenSpotsMessage()
        # If theres an open
        if not message == "":
            print(message)


    # Does a check run every 20 minutes until 10 minutes from the open time.
    while(tdelta > timedelta(minutes=10)):
        # Checks class item.
        for classItem in classes:
            checkClassRun(classItem)
            message = classItem.onlyOpenSpotsMessage()

            # If theres an open
            if not message == "":
                print(message)

        # Updates tDelta every minute.
        for i in range(20):
            currTime = datetime.now()
            tdelta = configs.openTime - currTime
            print("Time until open: " + str(tdelta))
            if(tdelta < timedelta(minutes=10)):
                break
            else:
                time.sleep(60)
        
    print("--------------------10 Minutes from opening checkpoint.----------------------")

    # Waits until 5 minutes before go time.
    while(tdelta > timedelta(minutes=5)):
            currTime = datetime.now()
            tdelta = configs.openTime - currTime
            print("Time until open: " + str(tdelta))
            if(tdelta < timedelta(minutes=5)):
                break
            else:
                time.sleep(30)

    print("--------------------5 Minutes from opening checkpoint.----------------------")


    # Waits until 1 minutes before go time.
    while(tdelta > timedelta(minutes=1)):
            currTime = datetime.now()
            tdelta = configs.openTime - currTime
            print("Time until open: " + str(tdelta))
            if(tdelta < timedelta(minutes=1)):
                break
            else:
                time.sleep(15)

    print("--------------------1 Minutes from opening checkpoint.----------------------")

    crns = []

    # Creates list of CRNs to be added.
    for classItem in classes:
        crns.append(classItem.checkAdd())
        print("CRNs to be added: ")
        print(classItem.checkAdd())

    # goes to add all crns.
    classBrowser.waitAddClass(crns)


    #TODO. Registration time is starting soon so i can't work on this for the time being.
    print("Check classes!")
        

def main(): 
    # Opens configuration file
    global configs
    configs = ConfigReader("config_angelo.ini")
    # Make sure to change this to whatever your config file is

    # Opens the browser
    global classBrowser
    classBrowser = Classer(configs.user, configs.password)

    # Gets classes from the config reader
    global classes
    classes = configs.classes

    # Initialization step.
    for classItem in classes:
        print("Initializing: " + classItem.subjectAbbr, classItem.courseNumber)
        # Initializing CRNs
        if(classItem.sectionNumbers[0] == "ALL"):
            crns, courses, openspots = classBrowser.getData(classItem.subjectAbbr, classItem.courseNumber)        
            classItem.setSectionNums(courses)
            classItem.setCRNs(crns)
            classItem.updateRemainingSpots(openspots)
        else:
            crns, crsNums, openspots = classBrowser.getData(classItem.subjectAbbr, classItem.courseNumber, classItem.sectionNumbers)
            classItem.setSectionNums(crsNums) 
            classItem.setCRNs(crns)
            classItem.updateRemainingSpots(openspots)

    print("CLASS DATA INITIALIZED!")


    # This part checks if registration is already open.
    global currTime
    currTime = datetime.now()

    # Checks time in relation to when the registration time opens.
    if(currTime < configs.openTime):
        print("Registration not open yet! Will check classes.")
        beforeOpenLoop()

    else:
        print("Registration already open. Starting checks")
        normalLoop()






if __name__ == "__main__":
    main()