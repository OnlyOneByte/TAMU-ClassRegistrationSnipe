import sys
from ClassObj import TAMUClass


class ConfigReader:

    def __init__(self, pathToConfigFile):
        config = open(pathToConfigFile, "r+")

        data = config.readlines()

        config.close()

        self.user = data[0].strip("\n").split(",")[1]
        self.password = data[1].strip("\n").split(",")[1]
        self.emailFrom = data[2].strip("\n").split(",")[1]
        self.emailPass = data[3].strip("\n").split(",")[1]
        self.emailTo = data[4].strip("\n").split(",")[1]
        self.pollingRate = float(data[5].strip("\n").split(",")[1])
        # 7th line (index 6) is skipped.

        # Data must now be in pairs of two.
        self.readInClasses(data[7:])

    

    def readInClasses(self, lines):
        self.classes = []

        # Checks to see if theres an even amount of lines. REQUIRED.
        if(len(lines)%2 == 1):
            raise Exception("Your INI File is wrong. Please fix.")
        

        for i in range(int(len(lines)/2)):
            header = lines[2*i].strip("\n").split(",")
            courses = lines[2*i + 1].strip("\n").split(" ")
            print(header[2])

            specialCourses = []
            for j in range(len(courses)):
                if courses[j][:1]=="*":
                    specialCourses.append(courses[j][:-1])
                    courses[j] = courses[j][:-1]
                    
            
            if len(specialCourses) > 0 and len(header) == 3:
                classTemp = TAMUClass(header[0].strip(" "), header[1].strip(" "), courses, classConflict=header[2].strip(" "), specialCourses=specialCourses)
                print("YEEE")
            elif len(specialCourses) > 0:
                classTemp = TAMUClass(header[0].strip(" "), header[1].strip(" "), courses, specialCourses=specialCourses)
            elif len(header) == 3:
                classTemp = TAMUClass(header[0].strip(" "), header[1].strip(" "), courses, classConflict=header[2].strip(" "))
            else:
                classTemp = TAMUClass(header[0].strip(" "), header[1].strip(" "), courses)

            
            
            self.classes.append(classTemp)

    sys.exit(0)



            