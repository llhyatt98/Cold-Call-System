"""
The main GUI window for selecting students V1.O
"""

import tkinter as tk
import time
import os
import threading

from backend.objects import Student, classQueue
from backend.control import *

USER_VIEW_OPEN = 0
USER_VIEW_WINDOW = None  # to pass user view window to HOME.py

def overwriteRosterFile(roster, studentQueue, delimiter="    "):
    ''' 
    This method overwrites the data held in the roster file. 
    The first line of the file is preserved, while the subsequent lines are replaced by the data held in the queue. 
    This method is called by both the up and down arrow keys, and is used to preserve data between sessions. 

    Args: roster, studentQueue, delimiter

    Returns:
    '''


    if len(studentQueue.queue) == 0:
        print("No data to log")

        # display error box
        title = 'No Data'
        heading = 'No data to log'
        msg = ''
        GUI.displayError(title, heading, msg)
        return

    try:
        with open(roster, "r") as f:
            header = f.readline()

        # Overwrite roster file, but preserve the first line
        with open(roster, "w") as f:
            f.write(header)
            
            d = delimiter
            for student in studentQueue.queue:
                dates = '['  + ' '.join(student.dates) + ']'
                line = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}\n".format(student.fname, d, student.lname, d, student.uoID, d,student.email, d, student.phonetic, d, student.reveal, d, student.numCalled, d, student.numFlags, d, dates)
                f.write(line)

    except FileNotFoundError:
        print('File Can\'t Be Opened')

        # display error box
        title = 'File Can\'t Be Opened'
        heading = 'Unable to open file'
        msg = 'File Can\'t Be Opened'
        GUI.displayError(title, heading, msg)
        return
    except:
        print('File Can\'t Be Opened')

        # display error box
        title = 'File Can\'t Be Opened'
        heading = 'Unable to open file'
        msg = 'File Can\'t Be Opened'
        GUI.displayError(title, heading, msg)
        return

class GUI:
    def __init__(self, winTitle: str, Roster):
        self.title = winTitle
        self.mainWindow = tk.Tk()
        global USER_VIEW_OPEN
        USER_VIEW_OPEN = 1

        self.canvas = tk.Label(self.mainWindow)
        self.button = tk.Button(self.canvas, text="EXIT", width=10, height=2, command=self.closeWindow)
        self.text = tk.Text(self.canvas, height=1, width=70, font=('Courier', 16))
        self.canvas.pack()
        self.text.pack()
        self.button.pack()

        self.mainWindow.title(self.title)  # set window title (grey bar at top)
        self.mainWindow.attributes("-topmost", True)  # keep the window in front of all other windows
        self.mainWindow.protocol("WM_DELETE_WINDOW", self.closeWindow)  # calls closeWindow() if user clicks red 'x'

        # for backend
        self.Roster = Roster             # creat a golable Roster which is a quene of a Student object
        self.onDeck = initDeck(self.Roster)     # 4 student object on deck, current_Index will be the index 
        self.current_Index = 0                  # the picked student's index in onDeck queue
        self.flagQ = classQueue()               # a list of student been flag 
        self.path = ""                         # path for the source file

    def closeWindow(self):
        self.mainWindow.destroy()
        global USER_VIEW_OPEN
        global USER_VIEW_WINDOW

        USER_VIEW_OPEN = 0
        USER_VIEW_WINDOW = None

    def leftKey(self, event):
        # print("Left key pressed")
        self.current_Index = left(self.current_Index, self.onDeck, self.Roster)
        names, highlightBegin, highlightEnd = OnDeckString(self.current_Index, self.onDeck)
        # print(names, highlightBegin, highlightEnd)
        self.update(names, highlightBegin, highlightEnd)

    def rightKey(self, event):
        # print("Right key pressed")
        self.current_Index = right(self.current_Index, self.onDeck, self.Roster)
        names, highlightBegin, highlightEnd = OnDeckString(self.current_Index, self.onDeck)
        # print(names, highlightBegin, highlightEnd)
        self.update(names, highlightBegin, highlightEnd)

    def upKey(self, event):
        # print("Up key pressed")
        self.current_Index = up(self.current_Index, self.onDeck, self.Roster, self.flagQ)
        names, highlightBegin, highlightEnd = OnDeckString(self.current_Index, self.onDeck)
        # print(names, highlightBegin, highlightEnd)
        self.update(names, highlightBegin, highlightEnd)
        overwriteRosterFile(self.path, self.Roster)


    def downKey(self, event):
        # print("Down key pressed")
        self.current_Index = down(self.current_Index, self.onDeck, self.Roster)
        names, highlightBegin, highlightEnd = OnDeckString(self.current_Index, self.onDeck)
        # print(names, highlightBegin, highlightEnd)
        self.update(names, highlightBegin, highlightEnd)
        overwriteRosterFile(self.path, self.Roster)

    def update(self, inText: str, highlightStart: int, highlightEnd: int, highlightColor='#23FF00'):
        """ Prints the names given in <inText> to the GUI screen.
        highlightStart is the starting index of the highlighting
        and highlightEnd is the ending index.
        """
        self.text.pack()
        self.text.configure(state='normal')  # reset state in order to change the names
        self.text.delete('1.0', tk.END)      # clear names
        self.text.insert('1.0', inText)      # write text to GUI
        self.text.configure(width=len(inText)+5)

        # now add highlighting
        self.text.tag_add('tag1', '1.{}'.format(highlightStart), '1.{}'.format(highlightEnd))
        self.text.tag_config('tag1', background=highlightColor)
        self.text.configure(state='disabled')  # prevents user from clicking and editing the text
        self.mainWindow.update()

def displayMessage(title: str, msg: str):
    os.system("""osascript -e 'display notification "{}" with title "{}"' """.format(msg, title))

def userViewOpen():
    return USER_VIEW_OPEN

def getUserViewWindow():
    return USER_VIEW_WINDOW

def testArrowKeys():
    """ Opens the GUI with 4 names, and the window remains unchanged.
    A message displays whenever an arrow key is pressed.
    """
    name1 = "Maura McCabe"
    name2 = "Jimmy Lam"
    name3 = "Lucas Hyatt"
    name4 = "Yin Jin"
    name5 = 'Noah Tigner'

    gui = GUI('Students on deck')

    print('--- Starting GUI test ---')

    names = "{}   {}   {}   {}".format(name1, name2, name3, name4)

    highlightBegin = len(name1) + 3
    highlightEnd = highlightBegin + len(name2)
    gui.update(names, highlightBegin, highlightEnd)

    # support for arrow key presses, bind() takes in function to use like pthread_create()

    gui.mainWindow.bind("<Left>", gui.leftKey)
    gui.mainWindow.bind("<Right>", gui.rightKey)
    gui.mainWindow.bind("<Up>", gui.upKey)
    gui.mainWindow.bind("<Down>", gui.downKey)

    print("\033[38;5;220mClick on the cold call window. After pressing an arrow key,",
          "\na message should be displayed. Close the cold call window to end the program.",
          "\nNote: the names and highlighting should not update for this test.\033[0m")

    gui.mainWindow.mainloop()  # blocks until the window is closed

def testScreenUpdate():
    """ Updates the names and highlighting."""
    name1 = "Maura McCabe"
    name2 = "Jimmy Lam"
    name3 = "Lucas Hyatt"
    name4 = "Yin Jin"
    name5 = 'Noah Tigner'

    gui = GUI('Students on deck')
    names = "{}   {}   {}   {}".format(name1, name2, name3, name4)

    highlightBegin = len(name1) + 3
    highlightEnd = highlightBegin + len(name2)
    gui.update(names, highlightBegin, highlightEnd)

    print('\nHighlighting moving to the right in 1 second...')
    time.sleep(1)

    highlightBegin = len(name1) + len(name2) + 6
    highlightEnd = highlightBegin + len(name3)
    gui.update(names, highlightBegin, highlightEnd)

    print('Removing Lucas in 1 second...')
    time.sleep(1)

    names = "{}   {}   {}   {}".format(name1, name2, name4, name5)

    highlightBegin = len(name1) + len(name2) + 6
    highlightEnd = highlightBegin + len(name4)
    gui.update(names, highlightBegin, highlightEnd)

    print("\n\033[38;5;220m--- End of test. Close the cold calling window to exit ---\033[0m")
    gui.mainWindow.mainloop()

def testcontrol(path, studentQ):
    global USER_VIEW_WINDOW

    # print('--- Starting control test ---')

    # print(type(path))

    studentQ.printQ()

    gui = GUI('Students on deck', studentQ)
    # print("Before Quene")
    # gui.Roster.printQ()
    gui.Roster = studentQ
    gui.path = path
    USER_VIEW_WINDOW = gui

    # print("self.Roster: ")
    # gui.Roster.printQ()


    names, highlightBegin, highlightEnd = OnDeckString(gui.current_Index, gui.onDeck)
    # print(names)

    gui.update(names, highlightBegin, highlightEnd)

    # support for arrow key presses, bind() takes in function to use like pthread_create()
    gui.mainWindow.bind("<Left>", gui.leftKey)
    gui.mainWindow.bind("<Right>", gui.rightKey)
    gui.mainWindow.bind("<Up>", gui.upKey)
    gui.mainWindow.bind("<Down>", gui.downKey)

    gui.mainWindow.mainloop()

def main():
    pass
    #testArrowKeys()
    #testScreenUpdate()
    #testcontrol()

