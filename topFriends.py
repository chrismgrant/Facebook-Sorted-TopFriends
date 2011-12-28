# topFriends.py
# Name: Christopher M. Grant
# AndrewID: cgrant

from Tkinter import *
import facebook
import tkMessageBox
import tkSimpleDialog
import os
import webbrowser

#exporting the TopFriendList as a text file using File IO
def getDesktopPath(filename = ""):
    # next line is odd, but works in Windows/Mac/Linux
    homepath = os.getenv('USERPROFILE') or os.getenv('HOME')
    return homepath + os.sep + "Desktop" + os.sep + filename

def fileExists(filename):
    return os.path.exists(filename)

def writeTextFile(text, filename):
    fileHandler = open(filename, "wt")
    fileHandler.write(text)
    fileHandler.close()
    
def exportTopFriendsList():
    #using FileIO, we grab our topFriendsList and then create a file of it
    #on our desktop
    topFriendsList = canvas.data.topFriendsList    
    n = ""
    for element in topFriendsList:
        n += element + "\n"
    writeTextFile(n, getDesktopPath("topFriendsList.txt"))

#functions for creating the TopFriendsList
def addFriend(username, friendList):
    graph = canvas.data.graph
    #each facebook friend is represented as a "graph" object under the
    #facebook api. we're using the get_object function in order to get our
    #friend, then we add them to the unsorted friendList
    friend = graph.get_object("/" + str(username))
    friendList.append(friend)

def sortFriendList(friendList):
    #creates a sorted idList after retrieving from each friend in friendList
    idList = canvas.data.idList
    for friend in friendList:
        idList.append(friend.items()[-1])
    idList.sort()        

def rankFriendList(friendList, idList):
    count = 0
    topFriendsList = canvas.data.topFriendsList
    #ranks each friend in friendList based on their corresponding id
    #then produces the topfriendsList
    for id in idList:
        for friend in friendList:
            if id[-1] == friend['id']:
                count += 1
                if 'link' in friend:
                    topFriendsList.append((str(count)) +". " +
                                          str(friend['name']) + ", "
                                          + friend['link'])
                elif 'username' in friend:
                    topFriendsList.append( str(count) + ". " +
                                           str(friend['name']) + ", " +
                                           "http://www.facebook.com/" +
                                           str(friend['username']))
                else:
                    topFriendsList.append(str(count) + ". " +
                                          str(friend['name']) + ", " +
                                          "htttp://www.facebook.com/" +
                                          "profile.php?id=" +
                                          str(friend['id']))
                                               
#Graphical User Interface Methods.
def drawBackground():
    canvas.create_rectangle(0,0, canvas.data.canvasWidth,
                            canvas.data.canvasHeight, fill="light blue")

def drawTopFriendsList():
    #draws the each ranked friend onto the canvas, with links next to them.
    #if link is pressed, call openBrowser(link)
    userImage = canvas.data.userImage
    userImageSize = ((userImage.width(), userImage.height()))
    topFriends = canvas.data.topFriendsList
    padding = 55
    width = canvas.data.canvasWidth
    height = canvas.data.canvasHeight
    n = len(topFriends)
    y = 115
    py = 60
    for n in xrange(len(topFriends)):    
            canvas.create_image(width / 2, y + (n*py), anchor = N,
                                image = userImage)
            canvas.create_text(width / 2, (y + (n*py)) + padding,
                               text = str(topFriends[n]),
                               font = "Helvetica 14", fill = "blue")
        
    

class AboutDialog(tkSimpleDialog.Dialog):
    #creates our about dialog prompt
    def body(self, master):
        description = "Have you ever wanted a top friends list of your \
facebook,\n but wanted a completely randomized order\nto make everyone feel of \
equal importance to you?\n Look no further than the Auto Friend Lister.\nSimply\
 choose the friends you want listed\nand the application will sort your\
\nfriends based on their unique facebook id values.\
\nYou can even save the list!"
        Label(master, text= "About:").grid(row= 0)
        Label(master,text= description, justify= CENTER).grid(row=1)

class GoDialog(tkSimpleDialog.Dialog):
    #creates our go dialog prompt
    def body(self, master):
        Label(master, text="Friend:").grid(row=0)
        self.e = Entry(master)
        self.e.grid(row=0, column=1)
    def apply(self):
        usernames = canvas.data.usernames
        usernames.append(self.e.get())

class MoreDialog(tkSimpleDialog.Dialog):
    #create our more dialog prompt
    def body(self, master):
        Label(master, text="Friend Link:").grid(row = 0)
        self.e = Entry(master)
        self.e.grid(row=1, column= 0)
    def apply(self):
        canvas.data.link = self.e.get()

def goPressed():
    #sends information from all text fields into addFriend calls, then
    #makes a call to sortFriendList, and finally rankFriendList. also calls
    #loadingScreen().
    friendList = canvas.data.friendList
    idList = canvas.data.idList
    usernames = canvas.data.usernames
    topFriendsList = canvas.data.topFriendsList
    canvas.data.mode = 2
    mode = canvas.data.mode
    loadingScreen()
    GoDialog(canvas)
    message = "Would you like to add another friend?"
    title = "More Friends?"
    response = tkMessageBox.askquestion(title, message)
    while str(response) == "yes":
        GoDialog(canvas)
        response = tkMessageBox.askquestion(title, message)
    for username in usernames:
        addFriend(username, friendList)
    sortFriendList(friendList)
    rankFriendList(friendList, idList)
    canvas.data.mode = 3
    redrawAll()

def aboutPressed():
    #if about button is pressed, opens a dialog with information about the
    #application.
    AboutDialog(canvas)
    redrawAll()

def backPressed():
    #calls init() if back button is pressed and sends user back to starting
    #point of the application. I.e. mode is reset to 1 and all user data is
    #erased.
    init()
    redrawAll()

def exportPressed():
    #If export button is pressed, call exportTopFriendsList() to create
    #the text file version of the Top Friends List on your desktop.
    exportTopFriendsList()

def openBrowser(link):
    #uses the webbrowser module to open your webbrowser
    webbrowser.open(link)

def morePressed():
    #responds to pressing the more button, to open the dialog, then browser
    MoreDialog(canvas)
    link = canvas.data.link
    openBrowser(link)
    redrawAll()

def loadingScreen():
    #after go button is pressed, paints a loading screen of just "loading.gif"
    #for 5 seconds. then calls drawTopFriendsList().
    canvas.delete(ALL)
    drawBackground()
    loader = canvas.data.loader
    loaderSize = ((loader.width(), loader.height()))
    width = canvas.data.canvasWidth
    height = canvas.data.canvasHeight
    canvas.create_text(width / 2, 400, text="Loading...",
                       font = "Courier 18 italic", fill = "white")
    canvas.create_image(width / 2, height / 3, anchor = N, image = loader)

def completeScreen():
    #draw rankedList, links, back and export buttons.
    canvas.delete(ALL)
    drawBackground()
    width = canvas.data.canvasWidth
    height = canvas.data.canvasHeight
    export = canvas.data.exportButton
    back = canvas.data.backButton
    more = canvas.data.moreButton
    topFriends = canvas.data.topFriendsList
    canvas.create_text(width / 2, 100, text = "Top Friends List:",
                       font = "Helvetica 36 underline", fill = "white")
    drawTopFriendsList()
    canvas.create_window(width- (width / 8), height - 20,
                         window = export)
    canvas.create_window((width / 8), height - 20, window = back)
    canvas.create_window(width/2, height - 20, window = more)
    

def mousePressed(event):
    #Not Used particularly for this 
    redrawAll()

def keyPressed(event):
    #if a particular sequence of keys are pressed, an easter egg appears.
    if event.char == "`":
        import invaders.py
        invaders.run()
    redrawAll()

def timerFired():
    #Not used particularly for this application.
    pass

def redrawAll():
    canvas.delete(ALL)
    mode = canvas.data.mode
    friendList = canvas.data.friendList
    idList = canvas.data.idList
    drawBackground()
    logo = canvas.data.logo
    logoSize = ((logo.width(), logo.height()))
    width = canvas.data.canvasWidth
    height = canvas.data.canvasHeight
    about = canvas.data.aboutButton
    go = canvas.data.goButton
    if mode == 1:
        canvas.create_image(width / 2, height / 3, anchor = N, image = logo)
        canvas.create_text(300, 400, text="Top Friends by ID",
                       font = "Helvetica 18 italic", fill = "white")
        canvas.create_window(420, 450, window = about)
        canvas.create_window(500, 450, window = go)
    elif mode == 2:
        loadingScreen()
    elif mode == 3:
        completeScreen()
    
def init():
    #we store our empty lists and set the default mode
    canvas.data.idList = []
    canvas.data.friendList = []
    canvas.data.topFriendsList = []
    canvas.data.usernames = []
    canvas.data.link = ""
    canvas.data.mode = 1
    #we store our images and buttons
    logo = PhotoImage(file="facebook-logo.gif")
    canvas.data.logo = logo
    loader = PhotoImage(file="loading.gif")
    canvas.data.loader = loader
    userImage = PhotoImage(file="user-logo.gif")
    canvas.data.userImage = userImage
    #storing the about, go, export, and back buttons
    aboutButtonImage = PhotoImage(file="aboutButton.gif")
    about = Button(canvas, image = aboutButtonImage, width = 45,
                height = 23, bg = "light blue", command = aboutPressed)
    about.image = aboutButtonImage
    canvas.data.aboutButton = about
    goButtonImage = PhotoImage(file="goButton.gif")
    go = Button(canvas, image = goButtonImage, width = 45,
                height = 23, bg = "light blue", command = goPressed)
    go.image = goButtonImage
    canvas.data.goButton = go
    exportButtonImage = PhotoImage(file="exportButton.gif")
    export = Button(canvas, image = exportButtonImage, width = 45, height = 23,
                    bg = "light blue", command= exportPressed)
    export.image = exportButtonImage
    canvas.data.exportButton = export
    backButtonImage = PhotoImage(file="backButton.gif")
    back = Button(canvas, image = backButtonImage, width = 45, height = 23,
                    bg = "light blue", command= backPressed)
    back.image = backButtonImage
    canvas.data.backButton = back
    moreButtonImage = PhotoImage(file="moreButton.gif")
    more = Button(canvas, image = moreButtonImage, width = 45, height = 23,
                  bg = "light blue", command = morePressed)
    more.image = moreButtonImage
    canvas.data.moreButton = more
    canvas.pack()
    redrawAll()

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    root.title('Facebook Automated Friend Ranker')
    canvasWidth = 550
    canvasHeight = 700
    canvas = Canvas(root, width= canvasWidth, height=canvasHeight)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    canvas.data.graph = facebook.GraphAPI()
    init()
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  
run()
