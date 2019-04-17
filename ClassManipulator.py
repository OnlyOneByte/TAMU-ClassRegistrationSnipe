import time
import smtplib
import sys
import re
import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import messagebox

class Classer:

    def __init__(self, username, password):

        self.timeBetweenAction=1

                # uses the old class search funciton
        # These are the elements added.
        self.classElems = {
            'ClassSearch' :"//*[@id='tamu-searchclasssche-icon']",
            'MiniFrame': "//iframe[@id='Pluto_92_ctf3_247668_tw_frame']",
            'TermSubmit': "//input[@type='submit' and @value='Submit']",
            'AdvancedSearch': "/html/body/div[3]/form[2]/div/input",
            'CourseNumberBox': "//*[@id='crse_id']",
            'SectionSearch' : "//*[@id='advCourseBtnDiv']/input",
            'SubjectAbbrev' : "/html/body/div[3]/form/table[1]/tbody/tr/td[2]/select/option[@value='",
            'TableRows' : "/html/body/div[3]/form/table/tbody/tr",
        }

        # xPaths to a bunch of things I need to navigate around.
        # They are here so I can easily edit them in case howdy changes.
        self.elems = {
            'howdyHome': "//*[@id='loginbtn']",
            'usernameBox': "//*[@id='username']",
            'passwordBox': "//*[@id='password']",
            'nextButton': "//button[@type='submit']",
            'recordTab': "My Record",
            'addDropButton': "Add or Drop Classes",
            'regClass': "//*[@title='Registration']",
            'termSubmit': "//input[@type='submit' and @value='Submit']",
            '2fa': "//iframe[@id='duo_iframe']",
            '2faButton': "/html/body/div[1]/div[1]/div/form/fieldset[2]/div[1]/button",
            'addedCoursesTable' : "/html/body/div[3]/form/table[1]/tbody/tr",
            'dropClassDropDown' : "//*[@id='action_id2']",
            'classChangeSubmit': "/html/body/div[3]/form/input[19]",
            'addCRNBox1': "//*[@id='crn_id1']"
        }

        self.browser = webdriver.Chrome(r"chromedriver.exe")
        self.user = username
        self.passwd = password

        self.loggedIn = False   
        self.twofa = False       

        self.errorsTotal = 0    # Total errors so far
        self.errorsReset = 25  # Errors before total reset.

        # Homescreeen once logged in.
        self.homeScreen = "https://howdy.tamu.edu/uPortal/f/welcome/normal/render.uP"


        # First, login. 
        self.login()


    """
    If the program ends up in some kind of exception loop, this program here is what should get it out of it.
    It waits for a page to definitely finish loading, then continues on its merry way
    """
    def reset(self):
        # Opens browser link
        time.sleep(30)
        self.browser.get(self.homeScreen)
        time.sleep(30)
        self.errorsTotal = 0    # Resets error count
        self.login()

    """
    This is just put at the end of every single except loop to show any errors that may have occured.
    TODO: Add logging.
    """
    def errorHandler(self, e):
        self.errorsTotal+=1
        print("Total Errors:", str(self.errorsTotal))
        if(self.errorsTotal > self.errorsReset):
            self.reset()
        print(e)
        traceback.print_exc
    
    """
    This function navigates through the howdy login system. Requires user-input for the 2fa.
    """
    def login(self):
        while (not self.loggedIn or not self.twofa):
            try:
                # Opens browser link
                self.browser.get("https://howdy.tamu.edu")
                time.sleep(self.timeBetweenAction)

                # Login sequence
                self.browser.find_element_by_xpath(self.elems['howdyHome']).click()
                time.sleep(self.timeBetweenAction)
                self.browser.find_element_by_xpath(self.elems['usernameBox']).send_keys(self.user)
                self.browser.find_element_by_xpath(self.elems['nextButton']).click()
                time.sleep(self.timeBetweenAction)
                self.browser.find_element_by_xpath(self.elems['passwordBox']).send_keys(self.passwd)
                self.browser.find_element_by_xpath(self.elems['nextButton']).click()
                
                # The 2fa module takes a bit to load. Give it extra time.
                time.sleep(2*self.timeBetweenAction)

                # 2FA sequence
                try:
                    duoFrame = self.browser.find_element_by_xpath(self.elems["2fa"])
                    usePush = True
                    if(usePush):
                        self.browser.switch_to.frame(duoFrame)
                        self.browser.find_element_by_xpath(self.elems["2faButton"]).click()

                        print("CHECK YOUR PHONE FOR PUSH NOTIF.")

                        # While not yet past 2fa page
                        while(len(self.browser.find_elements_by_xpath(self.elems['regClass'])) == 0):
                            time.sleep(1)
                        print("Got passed 2fa")


                    else:
                        # Legacy method.
                        messagebox.showinfo(title='2-step verification', message='Finish on screen 2-step verification, and then click OK.')
                    
                    self.twofa = True
                except:
                    # TODO better bad pass and user check
                    print("Whoops. no 2fa. Ignore if you've already done 2fa this specific run of the program")
                    pass
                

                # Toggles the logged in state to true, if registration button is found.
                self.loggedIn = True

            except Exception as e:
                self.errorHandler(e)
                print("Failed to login. Trying again...")
                pass

    """
    This program navigates to course search and grabs all relevant data about courses the user
    indicated they have an interest in.

    subAbbr: string. The class abbreviation (CHEM, MATH, ENGR, PHYS, etc)
    courseNumber: string. The # of the course (CHEM 117, course number would be 117)
    sections: [strings] - all the sections that you want to check
    """
    def getData(self, subAbbr, courseNumber, sections=[]):
        searchAll = len(sections) == 0  # Searches all if sections is empty
        crns = []
        openSpots = []

        if(not searchAll):
            crns = [""] * len(sections)
            openSpots = [0] * len(sections)
        
        # This is to see if its done.
        checkedClasses = False

        while (not checkedClasses):
            try:
                # Opens home screen
                self.browser.get(self.homeScreen)
                time.sleep(self.timeBetweenAction)

                # Opens new class search
                self.browser.find_element_by_xpath(self.classElems['ClassSearch']).click()
                time.sleep(self.timeBetweenAction)

                # Switches to the miniframe that TAMU uses on this page.
                iframe = self.browser.find_element_by_xpath(self.classElems["MiniFrame"])
                self.browser.switch_to.frame(iframe)
                time.sleep(self.timeBetweenAction)

                # Navigates to search function
                self.browser.find_element_by_xpath(self.classElems['TermSubmit']).click()
                time.sleep(2*self.timeBetweenAction)

                # Opens advanced Search
                self.browser.find_element_by_xpath(self.classElems['AdvancedSearch']).click()
                time.sleep(self.timeBetweenAction)

                # Search function using thing.
                subjectAbbr = self.classElems['SubjectAbbrev'] + subAbbr+"']"
                self.browser.find_element_by_xpath(subjectAbbr).click()
                self.browser.find_element_by_xpath(self.classElems['CourseNumberBox']).send_keys(courseNumber)
                self.browser.find_element_by_xpath(self.classElems['SectionSearch']).click()
                # At this point should have reached the course list
                time.sleep(self.timeBetweenAction)

                # rows of rable
                tableRows = self.browser.find_elements_by_xpath(self.classElems['TableRows'])

                for i in range(2, len(tableRows)):
                    # Gets section num and num remaining
                    sectionNum = tableRows[i].find_elements_by_tag_name("td")[4]
                    numRemaining = tableRows[i].find_elements_by_tag_name("td")[12]

                    # Some rows are padding for a class so this only finds rows with real classes.
                    if(re.search(r'\d', sectionNum.text)):
                        
                        # Searches all spections
                        if searchAll:
                            sections.append(sectionNum.text)
                            crns.append(tableRows[i].find_elements_by_tag_name("td")[1].text)
                            openSpots.append(int(numRemaining.text))

                        if not searchAll and sectionNum.text in sections:
                            crnSec = (tableRows[i].find_elements_by_tag_name("td")[1].text)
                            # Matches CRN to Section
                            crns[sections.index(sectionNum.text)] = crnSec
                            openSpots[sections.index(sectionNum.text)]= int(numRemaining.text)
                    

                    if(not searchAll and len([x for x in crns if not x== ""]) == len(sections)):
                        # If you aren't searching all this makes it move faster
                        break
                
                checkedClasses = True
            except Exception as e:
                self.errorHandler(e)
                print("Something went wrong searching for the class. Trying again.")
                # sys.exit(0)

        return crns, sections, openSpots


    """
    This function checks to see if the sections specified of a specific course have any openings.
    returns a list of openings that match in index with the sections array passed in.

    subAbbr: string. The class abbreviation (CHEM, MATH, ENGR, PHYS, etc)
    courseNumber: string. The # of the course (CHEM 117, course number would be 117)
    sections: [strings] - all the sections that you want to check
    """
    def checkSpots(self, subAbbr, courseNumber, sections):
        openSpots = [0]* len(sections)
        checked = 0


        # This is to see if its done.
        checkedClasses = False

        while (not checkedClasses):
            try:
                # Opens home screen
                self.browser.get(self.homeScreen)
                time.sleep(self.timeBetweenAction)

                # Opens new class search
                self.browser.find_element_by_xpath(self.classElems['ClassSearch']).click()
                time.sleep(self.timeBetweenAction)

                # Switches to the miniframe that TAMU uses on this page.
                iframe = self.browser.find_element_by_xpath(self.classElems['MiniFrame'])
                self.browser.switch_to.frame(iframe)
                time.sleep(self.timeBetweenAction)

                # Navigates to search function
                self.browser.find_element_by_xpath(self.classElems['TermSubmit']).click()
                time.sleep(2*self.timeBetweenAction)

                # Opens advanced Search
                self.browser.find_element_by_xpath(self.classElems['AdvancedSearch']).click()
                time.sleep(self.timeBetweenAction)

                # Search function using thing.
                subjectAbbr = self.classElems['SubjectAbbrev'] + subAbbr+"']"
                self.browser.find_element_by_xpath(subjectAbbr).click()
                self.browser.find_element_by_xpath(self.classElems['CourseNumberBox']).send_keys(courseNumber)
                self.browser.find_element_by_xpath(self.classElems['SectionSearch']).click()
                # At this point should have reached the course list
                time.sleep(self.timeBetweenAction)

                # rows of rable
                tableRows = self.browser.find_elements_by_xpath(self.classElems['TableRows'])

                for i in range(2, len(tableRows)):
                    sectionNum = tableRows[i].find_elements_by_tag_name("td")[4]
                    numRemaining = tableRows[i].find_elements_by_tag_name("td")[12]

                    if(re.search(r'\d', sectionNum.text)):
                        if(sectionNum.text in sections):
                            openSpots[sections.index(sectionNum.text)]= int(numRemaining.text)
                            checked+=1

                    # Finished checking
                    if(checked == len(sections)):
                        break

                
                checkedClasses = True
            except Exception as e:
                self.errorHandler(e)
                print("An error happened when refreshing open spots. Retrying.")
        return openSpots
    


    """
    This drops a class in order to replace it with a new one.

    cropCourseCRN: the CRN of the course to drop
    addCourseCRN: the CRN of the course to add.

    returns 0 if successful
    returns -1 if failed.

    """
    def dropThenAddClass(self, dropCourseCRN, addCourseCRN):
        # THis is to see if it finished dropping the class
        droppedClass = False

        # If successfully sniped. If it wasn't successfull, add the old class back
        success = False

        # This is to see if its done.
        addedClass = False

        while (not addedClass and not droppedClass):
            try:    
                self.browser.get(self.homeScreen)

                # Opens registration window.
                self.browser.find_element_by_xpath(self.elems['regClass']).click()
                time.sleep(self.timeBetweenAction)

                # Switches to the miniframe that TAMU uses on this page.
                iframe = self.browser.find_element_by_xpath(self.classElems['MiniFrame'])
                self.browser.switch_to.frame(iframe)

                # Clicks the submit button to access the courses.
                self.browser.find_element_by_xpath(self.elems['termSubmit']).click()
                time.sleep(self.timeBetweenAction)

                # Drops the class if it hasn't been dropped already.
                if(not droppedClass):
                    tableRows = self.browser.find_elements_by_xpath(self.elems['addedCoursesTable'])
                    for i in range(1,len(tableRows)):
                        rowCRN = tableRows[i].find_elements_by_tag_name("td")[2].text
                        if(dropCourseCRN == rowCRN):
                            # drop old class here
                            # Selects Drop
                            self.browser.find_element_by_xpath("//select[@id='action_id"+str(i)+"']/option[text()='DROP']").click()
                            break

                    # Submits changes             
                    self.browser.find_element_by_xpath(self.elems['classChangeSubmit']).click()
                    droppedClass = True
                    time.sleep(self.timeBetweenAction)
                


                # Adds CRN 
                self.browser.find_element_by_xpath(self.elems['addCRNBox1']).send_keys(addCourseCRN)
                self.browser.find_element_by_xpath(self.elems['classChangeSubmit']).click()
                time.sleep(self.timeBetweenAction)


                # Double checks to see if course was added.
                tableRows = self.browser.find_elements_by_xpath(self.elems["addedCoursesTable"])
                for i in range(1,len(tableRows)):
                    rowCRN = tableRows[i].find_elements_by_tag_name("td")[2].text
                    if(addCourseCRN == rowCRN):
                        print("SNIPED!")
                        success = True


                # If the program wasn't successful in a snipe, it adds the old course back
                if not success:
                    print("Wasn't successful. Adding old course back")
                    self.browser.find_element_by_xpath(self.elems['addCRNBox1']).send_keys(dropCourseCRN)
                    self.browser.find_element_by_xpath(self.elems['classChangeSubmit']).click()
                    return -1


                # Got to add/drop place
                addedClass = True
                # Submits changes
                time.sleep(self.timeBetweenAction)

            except Exception as e:
                self.errorHandler(e)
                print("An error happened when sniping spots. Retrying.")

        return 0



    """
    This just adds a class given its CRN

    addCourseCRN: the CRN of the course to add.

    returns 0 if successful
    returns -1 if failed.

    """
    def addClass(self, addCourseCRN):
        # This is to see if its done.
        finished = False

        while (not finished):
            try:    
                self.browser.get(self.homeScreen)

                # Opens registration window.
                self.browser.find_element_by_xpath(self.elems['regClass']).click()
                time.sleep(self.timeBetweenAction)

                # Switches to the miniframe that TAMU uses on this page.
                iframe = self.browser.find_element_by_xpath(self.classElems['miniFrame'])
                self.browser.switch_to.frame(iframe)

                # Clicks the submit button to access the courses.
                self.browser.find_element_by_xpath(self.elems['termSubmit']).click()
                time.sleep(self.timeBetweenAction)


                # Adds CRN 
                self.browser.find_element_by_xpath(self.elems['addCRNBox1']).send_keys(addCourseCRN)
                self.browser.find_element_by_xpath(self.elems['classChangeSubmit']).click()
                time.sleep(self.timeBetweenAction)


                # Double checks to see if course was added.
                tableRows = self.browser.find_elements_by_xpath(self.elems["addedCoursesTable"])
                for i in range(1,len(tableRows)):
                    rowCRN = tableRows[i].find_elements_by_tag_name("td")[2].text
                    if(addCourseCRN == rowCRN):
                        print("Success")
                        return 0
                # Got to add/drop place
                finished = True

            except Exception as e:
                self.errorHandler(e)
                print("An error happened when sniping spots. Retrying.")
        return -1



    """
    Keeps refreshing until open time.
    addCourseCRN: list CRNs to add.

    returns 0 if successful
    returns -1 if failed.

    """
    def waitAddClass(self, addCourseCRN):
        # This is to see if its done.
        finished = False

        while (not finished):
            try:    
                self.browser.get(self.homeScreen)

                # Opens registration window.
                self.browser.find_element_by_xpath(self.elems['regClass']).click()
                time.sleep(self.timeBetweenAction)

                # Switches to the miniframe that TAMU uses on this page.
                iframe = self.browser.find_element_by_xpath(self.classElems['MiniFrame'])
                self.browser.switch_to.frame(iframe)

                # Clicks the submit button to access the courses.
                self.browser.find_element_by_xpath(self.elems['termSubmit']).click()
                time.sleep(self.timeBetweenAction)

                boxes = ["//*[@id='crn_id1']",
                        "//*[@id='crn_id2']",
                        "//*[@id='crn_id3']",
                        "//*[@id='crn_id4']",
                        "//*[@id='crn_id5']",
                        "//*[@id='crn_id6']",
                        "//*[@id='crn_id7']",
                        "//*[@id='crn_id8']",
                        "//*[@id='crn_id9']",
                        "//*[@id='crn_id10']"
                ]

                # Refreshes page every 2 seconds.
                while(len(self.browser.find_elements_by_xpath(boxes[0])) == 0):
                    time.sleep(1)
                    self.browser.refresh()
                    self.browser.find_element_by_xpath(self.elems['termSubmit']).click()
                    time.sleep(self.timeBetweenAction)

                # Adds CRN 
                for i in range(len(addCourseCRN)):
                    self.browser.find_element_by_xpath(boxes[i]).send_keys(addCourseCRN[i])

                self.browser.find_element_by_xpath(self.elems['classChangeSubmit']).click()
                time.sleep(self.timeBetweenAction)


                # Double checks to see if course was added.
                tableRows = self.browser.find_elements_by_xpath(self.elems['addedCoursesTable'])
                for i in range(1,len(tableRows)):
                    rowCRN = tableRows[i].find_elements_by_tag_name("td")[2].text
                    if(addCourseCRN == rowCRN):
                        print("Success")
                        return 0
                # Got to add/drop place
                finished = True

            except Exception as e:
                self.errorHandler(e)
                print("An error happened when sniping spots. Retrying.")
        return -1

    """
    This function sends an email to the user notifying them of openings in classes that they want
    message: string of message generated.
    emailTo: string email of recipient
    emailFrom: string email of sender
    emailPassword: string sender's password
    """
    def emailNotif(self, message, emailTo, emailFrom, emailPassword):
        # Emails you about the new spot
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(emailFrom, emailPassword)
        server.sendmail(emailFrom, emailTo, message)
        server.quit()
