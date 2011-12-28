Read Me  
Installation:
Part 1 - Installing the Facebook API for Python:
As for installing this module:
1. What you need to do is download the api from here:
 https://github.com/facebook/python-sdk

2. save that folder to either your desktop or wherever.

3. open up command prompt or whichever terminal you use.

cd to the specific folder: 
	e.g. "cd facebook-python-sdk-322930c"
	ex. You stored the folder on the desktop.  
You would open command prompt. type "cd desktop". then you would do "cd facebook-python-sdk-322930c".

after that you would use the command 
"python setup.py install"

Troubleshooting - Importing the Module:
simply say "import facebook" in a python shell.  <---If you have problems here, then you’ll know whether you have installed the module correctly. 

Running the application:
Simply run the topFriends.py file. 
	When the application runs, you should be able to click the about button to read about the application and start the application with the go button. From there, a loading screen will appear along with a prompt for a particular friend. You will answer the prompt with the facebook username or id of your particular.
For example: 
A user with the page, “facebook.com/cmgrant”, corresponds to a username of “cmgrant”.
For users that have a page of “facebook.com/profile.php?id=500641353”, the corresponding username is that particular id number of “500641353”.
After each user entered, you have the option to add more or not. 
When you’re done, the produced ranked top friends list based upon least to greatest user id is presented. 
The user now has the option to go back and restart with the back button, export the top friends list as a text file on their desktop with the export button, or open the particular facebook page of a friend on the list via the default webbrowser through the more button.

P.S. There is a secret easter egg that opens the game invaders (invaders.py) if you press “ ` ”. 
Christopher M. Grant