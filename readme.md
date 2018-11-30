# Check the config.ini file to see how to use it.
# Must have Chrome and would also recommend Anaconda ver of Python 3.

yeeeeeee hawwwwwwww
last officially confirmed working 2018-11-29.
I'll maintain this for as long as I'm a student at TAMU and I have to use their godforsaken registration system.

# The INI file is laid out as follows.
line 1: username to howdy\
line 2: password to howdy\
line 3: email from which the email will BE SENT. I recommend creating a throwaway email for this purpose.\
line 4: email password.\
line 5: email of recipient. So your email, or whatever email you check often.\
line 6: polling timeout. The timeout between consecutive passes.\
line 7: ignored. Nothing here

All lines for classes are PAIRED.
You can add as many classes as you want.

For the first line, include the class subject abbreviation and the class number.\
If you have a class that you have to drop in order to pick this up, include the CRN of the class you need to drop after\
>MATH,152,18893\
^ The above means that I want a math 152 class, but I have to drop class CRN 18893 in order to get one\
>Math,152\
^ That just means either: Don't auto add classes, or no need to drop before adding

For the second line, its just a list of all the section numbers that you woudl want, seperated with spaces
>102 103 105 109

Or, if you just want to check every section, put ALL\
>ALL

If theres a section that you would want the auto add to work on, simply put a start after it.\
>102 103 105* 109

^ That just means that if 105 was availible, auto register me please. If none are selected, no auto-registration will happen.

I recommend you only star 1 section per class, but the program can handle multiple stars per class.

NOTE: Section nums must be 3 digits long. If you have a 2 digit sction number (like 63) put a zero in front! (063)
NOTE2: ANY CHANGES TO INI FILE REQUIRE A RESTART OF THE PROGRAM. (currently)



# TO SEND EMAILS YOUR GMAIL ACCOUNT NEEDS TO ALLOW LESS SECURE APPS
https://myaccount.google.com/lesssecureapps?pli=1

Also the emails are very likely to be marked as spam for some reason. (Mine was). Make sure to tell google that its not spam =(




inspired by the work of r3ledbetter: https://github.com/r3ledbetter/TAMU-Registration