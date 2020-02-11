'''
Author: Lucas Hyatt
'''


'''======================================Imports=========================================='''
import tkinter as tk
from tkinter import filedialog, Text, messagebox
import tkinter.ttk as ttk
import tkinter.font
import os
import GUI
import sys
from datetime import datetime
from backend.objects import Student, classQueue


'''======================================Functions=========================================='''

STUDENTQUEUE = classQueue()
ROSTERPATH = "" # global roster path, set by inputFile

def switch_view():
    global ROSTERPATH

    if ROSTERPATH is not None and 'config.txt' in ROSTERPATH:
        ROSTERPATH = ''

    if not GUI.userViewOpen():  # prevent 2 user view windows from opening simultaneously
        if ROSTERPATH != '' and ROSTERPATH is not None:
            GUI.testcontrol(ROSTERPATH, STUDENTQUEUE)
        else:
            messageBox = tk.messagebox.askokcancel('Load class roster', 'Please select a class roster', icon='info')
            if messageBox:
                inputFile()
            else:
                return
            if ROSTERPATH != '' and ROSTERPATH is not None:
                GUI.testcontrol(ROSTERPATH, STUDENTQUEUE)
            elif ROSTERPATH == '':
                return
            else:
                heading = 'Unable to open file'
                msg = 'Could not open the roster file'
                GUI.displayMessage(heading, msg)

def inputFile(firstTime=False, delimiter=None):
    ''' 
    This method reads student data line by line from a roster file.
    Each line is parsed and used to create a Student object, which is added to the global STUDENTQUEUE data structure.
    
    Args:   firstTime, a boolean representing if this method has been called before
            delimiter, a string. By default, lines are split by whitespace, but commas may also be specified
    
    Returns:
    '''

    global ROSTERPATH, STUDENTQUEUE

    if not ROSTERPATH or not firstTime:

        if len(STUDENTQUEUE.queue) > 0:
            # Warn the user before overwriting STUDENTQUEUE
            messageBox = tk.messagebox.askquestion('Load New Data', 'Are you sure you want to load in a new file?', icon = 'warning')
            if messageBox == 'no':
                return

        # Prompt the user to select a txt file
        filepath = filedialog.askopenfilename(initialdir="./..", title="Select File")
        if filepath == '':
            return

        if 'config.txt' in filepath:
            print("can't open configuration file as a roster")
            GUI.displayMessage('Not a roster file', 'config.txt is not a valid roster')
            ROSTERPATH = None
            setSettings(None)
            return

        ROSTERPATH = filepath
        setSettings(filepath)
        STUDENTQUEUE = classQueue() # Overwrite the queue

    if ROSTERPATH[-4:] != '.txt' or ".txt" not in ROSTERPATH:
        print('File must be a text file')
        GUI.displayMessage('Unable to open file', 'File must be a text file')

    try:
        with open(ROSTERPATH, "r") as f:
            next(f)     # skip first line of roster file (comments)
            for i, line in enumerate(f):

                elements = line.strip().split(delimiter)

                # print(elements)

                try:
                    fname = str(elements[0])
                    lname = str(elements[1])
                    uoID = int(elements[2])
                    email = str(elements[3])
                    phonetic = str(elements[4])
                    reveal = 0

                    if len(elements) >= 9:
                        
                        numCalled = int(elements[6])
                        numFlags = int(elements[7])

                        # Sort Dates Chronologically
                        dates = list(" ".join(elements[8:]).replace("[", "").replace("]", "").split())
                        dates = [datetime.strptime(date, "%d/%m/%y") for date in dates]
                        dates.sort(key = lambda date: date)
                        dates = [date.strftime("%d/%m/%y") for date in dates]
                        # dates = '['  + ' '.join(dates) + ']'
                        
                    else:
                        numCalled = 0
                        numFlags = 0
                        dates = []

                    # Create Student object, Insert into Queue
                    STUDENTQUEUE.enqueue(Student(fname, lname, uoID, email, phonetic, reveal, numCalled, numFlags, dates))

                except (ValueError, IndexError):
                    print("Line {} of roster file is formatted incorrectly".format(i+1))

                    # Reset these in case of a bad input file
                    ROSTERPATH = None
                    setSettings(None)

                    # display error box
                    heading = 'Unable to open file'
                    msg = 'Line {} is formatted incorrectly'.format(i+1)
                    GUI.displayMessage(heading, msg)
                    return

    except FileNotFoundError:
        print('File Can\'t Be Opened')

        # Reset these in case of a bad input file
        ROSTERPATH = None
        setSettings(None)

        # display error box
        heading = 'Unable to open file'
        msg = "File Cannot Be Opened"
        GUI.displayMessage(heading, msg)
        return
    except:
        print('File Can\'t Be Opened')

        # Reset these in case of a bad input file
        ROSTERPATH = None
        setSettings(None)

        # display error box
        heading = 'Unable to open file'
        msg = "File Cannot Be Opened"
        GUI.displayMessage(heading, msg)
        return

    # STUDENTQUEUE.printQ()

def writeSummaryPerformanceFile():
    ''' 
    This method writes to SummaryPerformanceFile.txt.
    The data of each student is written.
    The format of each line is specified by the header variable below
    
    Args: 
    
    Returns:
    '''

    global STUDENTQUEUE

    filepath = "../SummaryPerformanceFile.txt"
    header = "Summary Performance File for the Cold-Call-Assist program. Number-of-Times-Called    Number-of-Flags    First-Name    Last-Name    UO-ID    Email    Phonetic-Spelling    Reveal-Code    List-of-Dates\n"

    try:
        with open(filepath, "w") as f:
            f.write(header)

            for student in STUDENTQUEUE.queue:
                line = student.summaryPerformance()
                f.write(line)

        return 1

    except FileNotFoundError:
        print('File Can\'t Be Opened')

        # display error box
        heading = 'Unable to open file'
        msg = "File Cannot Be Opened"
        GUI.displayMessage(heading, msg)
        return 0
    except:
        print('File Can\'t Be Opened')

        # display error box
        heading = 'Unable to open file'
        msg = "File Cannot Be Opened"
        GUI.displayMessage(heading, msg)
        return 0

def writeLogFile():
    ''' 
    This method writes to dailyLogFile.txt.
    Only the data of students whose reveal code is 1 are written.
    
    Args: 
    
    Returns:
    '''

    global STUDENTQUEUE

    if len(STUDENTQUEUE.queue) == 0:
        print("No data to log")

        # display error box
        title = 'No Data'
        heading = 'No data to log'
        GUI.displayMessage(title, heading)
        return 0

    filepath = "../dailyLogFile.txt"
    date = datetime.now().strftime("%d/%m/%y %H:%M")
    header = "Log File. Last Modified " + date + "\n"

    try:
        with open(filepath, "w") as f:
            f.write(header)

            now = datetime.now().strftime("%d/%m/%y")
            for student in STUDENTQUEUE.queue:
                if now in student.dates:
                    x = 'X' if student.reveal else ' '
                    line = "{}    {} {} <{}>\n".format(x, student.fname, student.lname, student.email)
                    f.write(line)

        return 1

    except FileNotFoundError:
        print('File Can\'t Be Opened')

        # display error box
        heading = 'Unable to open file'
        msg = "File Cannot Be Opened"
        GUI.displayMessage(heading, msg)
        return 0
    except:
        print('File Can\'t Be Opened')

        # display error box
        heading = 'Unable to open file'
        msg = "File Cannot Be Opened"
        GUI.displayMessage(heading, msg)
        return 0

def getSettings():
    ''' 
    This method attempts to open config.txt and retreive the path to the roster data file.
    config.txt only exists after the first call to setSettings(), so this method is epected to fail on its first call
    
    Args: 
    
    Returns: 1 if successful, else nothing
    '''

    global ROSTERPATH

    config = "../config.txt"

    try:
        with open(config, "r") as f:
            path = next(f)
            if os.path.isfile(path):
                ROSTERPATH = path
                return 1
    except:
        # We don't need a popup here, this should happen in the background
        print("Unable to read settings from config.txt")

def setSettings(path):
    ''' 
    This method writes the path of the roster file to config.txt, where it can be read by getSettings(). 
    This function is called after the user selects a valid .txt file from the file selection window
    
    Args: path, the path to the roster data
    
    Returns: 
    '''

    config = "../config.txt"
    try:
        with open(config, "w") as f:
            f.write(path)

    except FileNotFoundError:
        print('File Can\'t Be Opened')

        # display error box
        heading = 'Unable to open file'
        msg = "File Cannot Be Opened"
        GUI.displayMessage(heading, msg)
        return
    except:
        print('File Can\'t Be Opened')

        # display error box
        heading = 'Unable to open file'
        msg = "File Cannot Be Opened"
        GUI.displayMessage(heading, msg)
        return

def exports():
    '''
    This is a simple helper function which we use to write to both log files during usage. 
    This function is called when a user presses keys associated to flagging a student or in any way adjusting their student data within the queue

    Args: 

    Returns: 
    '''
    summarySuccess = writeSummaryPerformanceFile()
    dailySuccess = writeLogFile()

    if summarySuccess and dailySuccess:
        GUI.displayMessage('Done exporting log files', '')

def openDaily(): # Opens the daily log file
    val = os.system("open ./../dailyLogFile.txt")
    if val == 256:
        heading = 'Unable to open Daily Log File'
        msg = 'Please press Export to Logs to generate the file'
        GUI.displayMessage(heading, msg)

def openSummary(): # Opens the summary log file
    val = os.system("open ./../SummaryPerformanceFile.txt")
    if val == 256:
        heading = 'Unable to open Performance File'
        msg = 'Please press Export to Logs to generate the file'
        GUI.displayMessage(heading, msg)

def exitProgram():
    window = GUI.getUserViewWindow()  # USER_VIEW_WINDOW global var must be set right after creating window
    #errorWin = GUI.getErrorWindow()
    if window is not None:
        window.closeWindow()
    #if errorWin is not None:
    #    errorWin.closeBox()
    root.destroy()


# Attempt to read default roster path from config.txt (this will fail the first time the program is run)

if getSettings():
    inputFile(firstTime=True)

'''======================================GUI=========================================='''

'''
Color Scheme:

red = #ff0443
blue = #0486ff
yellow = #ffde04
'''

#Creating a root and initializing attributes (foundation for GUI)
root = tk.Tk() #Establishes structure for app window
root.resizable(False, False)
root.title("Cold Call System")
root.attributes("-topmost", True)  # open window in front
root.protocol("WM_DELETE_WINDOW", exitProgram)  # calls closeWindow() if user clicks red 'x'

#Initializing pane to attach buttons and label to
pane = tk.Frame(root, bg = '#0486ff', bd=30)
pane.pack(fill = tk.BOTH, expand = True)

#Initializing font for the buttons.
button_font = tkinter.font.Font(family="Helvetica",size=20,weight="bold")
label_font = tkinter.font.Font(family="Helvetica",size=25,weight="bold")

#Progress bar will show how many student out of the roster have been chosen.
'''progress = ttk.Progressbar(pane, orient=tk.HORIZONTAL, length=496)
progress['value'] = 25
progress.pack(side=tk.BOTTOM)'''

#Label for the HOME MENU
label = tk.Label(pane, text="HOME MENU", bg='#0486ff')
label['font'] = label_font
label.grid(row=0, column=0)

#Button for the user view
user_view = tk.Button(pane, pady=8, width=16, text="User View", highlightbackground='#0486ff', command=switch_view)
user_view['font'] = button_font
user_view.grid(row=1, column=0)

#Button for inputting a roster
input_roster = tk.Button(pane, pady=8, width=16, text="Import New Roster", highlightbackground='#0486ff', command=inputFile)
input_roster['font'] = button_font
input_roster.grid(row=2, column=0)

#Button for exporting to logs
export_calls = tk.Button(pane, pady=8, width=16, text="Export to Logs", highlightbackground='#0486ff', command=exports)
export_calls['font'] = button_font
export_calls.grid(row=3, column=0)

#Button for displaying the daily log
daily_log = tk.Button(pane, pady=8, width=16, text="Daily Log File", highlightbackground='#0486ff', command=openDaily)
daily_log['font'] = button_font
daily_log.grid(row=4, column=0)

#Button for the displaying the summary performance file
summary_performance = tk.Button(pane, pady=8, width=16, text="Performance File", highlightbackground='#0486ff', command=openSummary)
summary_performance['font'] = button_font
summary_performance.grid(row=5, column=0)

#Button for exiting and closing the program (all windows)
exit_menu = tk.Button(pane, pady=8, width=16, text="Exit Program", highlightbackground='#0486ff', fg='red', command=exitProgram)
exit_menu['font'] = button_font
exit_menu.grid(row=6, column=0)

# Main Loop
root.update()
root.attributes("-topmost", False)  # allow window to go behind other windows
root.mainloop()
exit()















