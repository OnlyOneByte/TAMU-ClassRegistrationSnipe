import time
import smtplib
import sys
import re
import traceback
from selenium import webdriver
from tkinter import messagebox


class Classer:

    def __init__(self, username, password):

        self.timeBetweenAction=0.1

        # Xpaths to a bunch of things I need to navigate around.
        self.elems = {'howdyHome': "//*[@id='loginbtn']",
            'usernameBox': "//*[@id='username']",
            'passwordBox': "//*[@id='password']",
            'nextButton': "//button[@type='submit']",
            'recordTab': "My Record",
            'addDropButton': "Add or Drop Classes",
            'regClass': "//*[@title='Registration']",
            'miniFrame': "//iframe[@id='Pluto_92_ctf3_247668_tw_frame']",
            'termSubmit': "//input[@type='submit' and @value='Submit']",
            'classSearch': "/html/body/div[3]/form/input[20]",
            'advancedSearch': "/html/body/div[3]/form[2]/span/input",
            '2fa': "//iframe[@id='duo_iframe']",
            '2faButton': "//*[@class='icon-smartphone-check']",
            'courseNumberBox': "//*[@id='crse_id']",
            'sectionSearch' : "//*[@id='advCourseBtnDiv']/input"
        }
        self.browser = webdriver.Chrome(r"C:/Users/Angelo/Desktop/chromedriver.exe")
        self.user = username
        self.passwd = password

        self.loggedIn = False  # TODO add logged out checker
        self.twofa = False       # TODO 2fa

        # First, login. 
        self.login()

    
    # Should end at home page.
    def login(self):
        while (not self.loggedIn and not self.twofa):
            try:
                # Opens browser link
                self.browser.get("https://howdy.tamu.edu")

                # Login sequence
                self.browser.find_element_by_xpath(self.elems['howdyHome']).click()
                time.sleep(self.timeBetweenAction)
                self.browser.find_element_by_xpath(self.elems['usernameBox']).send_keys(self.user)
                self.browser.find_element_by_xpath(self.elems['nextButton']).click()
                time.sleep(self.timeBetweenAction)
                self.browser.find_element_by_xpath(self.elems['passwordBox']).send_keys(self.passwd)
                self.browser.find_element_by_xpath(self.elems['nextButton']).click()
                time.sleep(self.timeBetweenAction)

                # 2FA sequence
                try:
                    self.browser.find_element_by_xpath(self.elems["2fa"])
                    # TODO automate the 2fa process more
                    messagebox.showinfo(title='2-step verification', message='Finish on screen 2-step verification, and then click OK.')
                    self.twofa = True
                except:
                    # TODO better bad pass and user check
                    print("Check your password or username.")
                    pass
                

                # Toggles the logged in state to true.
                self.loggedIn = True

            except Exception as e:
                print(e)
                traceback.print_exc
                print("Failed to login. Trying again...")
                pass

    #
    # Get all relevant data for a course. Used in initialization
    #
    def getData(self, subAbbr, courseNumber, sections=None):
        if(sections==None):
            sections = []

        searchAll = len(sections) == 0  # Searches all if sections is empty
        openSpots = []
        crns = []
        
        # Sorts array.
        if not searchAll:
            sections = [int(i) for i in sections]
            sections.sort()
            sections = [str(i) for i in sections]


        # This is to see if its done.
        checkedClasses = False

        # Opens the home screens
        homeScreen = "https://howdy.tamu.edu/uPortal/f/welcome/normal/render.uP"

        while (not checkedClasses):
            try:    
                self.browser.get(homeScreen)
                time.sleep(self.timeBetweenAction)
                # Opens registration window.
                self.browser.find_element_by_xpath(self.elems['regClass']).click()

                # Switches to the miniframe that TAMU uses on this page.
                iframe = self.browser.find_element_by_xpath(self.elems["miniFrame"])
                self.browser.switch_to.frame(iframe)

                time.sleep(2*self.timeBetweenAction)

                # Navigates to search function
                self.browser.find_element_by_xpath(self.elems['termSubmit']).click()
                time.sleep(self.timeBetweenAction)

                self.browser.find_element_by_xpath(self.elems['classSearch']).click()
                time.sleep(self.timeBetweenAction)

                self.browser.find_element_by_xpath(self.elems['advancedSearch']).click()
                time.sleep(self.timeBetweenAction)

                # Search function using thing.
                subjectAbbr = "/html/body/div[3]/form/table[1]/tbody/tr/td[2]/select/option[@value='"+ subAbbr+"']"
                self.browser.find_element_by_xpath(subjectAbbr).click()
                self.browser.find_element_by_xpath(self.elems['courseNumberBox']).send_keys(courseNumber)
                self.browser.find_element_by_xpath(self.elems['sectionSearch']).click()
                # At this point should have reached the course list
                time.sleep(self.timeBetweenAction)

                # rows of rable
                tableRows = self.browser.find_elements_by_xpath("/html/body/div[3]/form/table/tbody/tr")

                for i in range(2, len(tableRows)):
                    # Gets section num and num remaining
                    sectionNum = tableRows[i].find_elements_by_tag_name("td")[4]

                    if(re.search(r'\d', sectionNum.text)):
                        if searchAll:
                            sections.append(sectionNum.text)
                            openSpots.append(int(tableRows[i].find_elements_by_tag_name("td")[12].text))
                            crns.append(tableRows[i].find_elements_by_tag_name("td")[1].text)

                        if not searchAll and sectionNum.text in sections:
                            openSpots.append(int(tableRows[i].find_elements_by_tag_name("td")[12].text))
                            crns.append(tableRows[i].find_elements_by_tag_name("td")[1].text)

                
                checkedClasses = True
            except Exception as e:
                print(e)
                traceback.print_exc
                print("Something went wrong searching for the class. Trying again.")
                # sys.exit(0)

        if not searchAll:
            sections = [int(i) for i in sections]
            sections.sort()
            sections = [str(i) for i in sections]



        return crns, sections, openSpots


    # returns lists of crns and courses.
    def checkSpots(self, subAbbr, courseNumber, sections):
        openSpots = []


        # This is to see if its done.
        checkedClasses = False

        # Opens the home screen
        homeScreen = "https://howdy.tamu.edu/uPortal/f/welcome/normal/render.uP"

        while (not checkedClasses):
            try:    
                self.browser.get(homeScreen)

                # Opens registration window.
                self.browser.find_element_by_xpath(self.elems['regClass']).click()
                time.sleep(self.timeBetweenAction)

                # Switches to the miniframe that TAMU uses on this page.
                iframe = self.browser.find_element_by_xpath(self.elems["miniFrame"])
                self.browser.switch_to.frame(iframe)


                # Navigates to search function
                self.browser.find_element_by_xpath(self.elems['termSubmit']).click()
                time.sleep(self.timeBetweenAction)
                self.browser.find_element_by_xpath(self.elems['classSearch']).click()
                time.sleep(self.timeBetweenAction)
                self.browser.find_element_by_xpath(self.elems['advancedSearch']).click()
                time.sleep(self.timeBetweenAction)

                # Search function using thing.
                subjectAbbr = "/html/body/div[3]/form/table[1]/tbody/tr/td[2]/select/option[@value='"+ subAbbr+"']"
                self.browser.find_element_by_xpath(subjectAbbr).click()
                self.browser.find_element_by_xpath(self.elems['courseNumberBox']).send_keys(courseNumber)
                self.browser.find_element_by_xpath(self.elems['sectionSearch']).click()
                time.sleep(self.timeBetweenAction)
                
                # At this point should have reached the course list

                # rows of table
                
                tableRows = self.browser.find_elements_by_xpath("/html/body/div[3]/form/table/tbody/tr")

                for i in range(2, len(tableRows)):
                    sectionNum = tableRows[i].find_elements_by_tag_name("td")[4]
                    numRemaining = tableRows[i].find_elements_by_tag_name("td")[12]

                    if(re.search(r'\d', numRemaining.text)):
                       if(sectionNum.text in sections):
                            openSpots.append(int(numRemaining.text))

                
                checkedClasses = True
            except Exception as e:
                print(e)
                print("An error happened when refreshing open spots. Retrying.")

        return openSpots


    # TODO: List all availible classes for one thign.
    def emailNotif(self, message, emailTo, emailFrom, emailPassword):
        # Emails you about the new spot
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(emailFrom, emailPassword)
        server.sendmail(emailFrom, emailTo, message)
        server.quit()
