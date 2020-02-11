Cold Calling Software
Author: Lucas Hyatt
Last Modified: 2/3/20

About
    The cold calling system developed in this project assists an instructor with
    calling on students in class. The system randomly selects four students from
    the class roster, and the names are displayed in a horizontal list. The
    instructor can then use the left/right arrow key to select a student, and an
    up (flag student) or down (no flag) key removes and replaces the student.

Directory Structure
    The main project directory (where README.txt is located) contains the majority
    of the text files used for the cold calling software. Once the program has been
    run at least once, the summary performance file and daily log file contain
    information about which students have been called on.

    The GUI subdirectory contains the source code for the software. It contains
    HOME.py and GUI.py which are responsible for the home menu interface and the
    cold calling list respectively. inside the GUI directory, the backend folder
    contains the student queue implementation and the functions to control it.

    If the program is run by opening the Cold Calling app, all the files used will
    be located in the Cold Call.app/Contents/Resources folder.
    
Running the software
    Once the group folder is unzipped, there will be a Cold Calling app and the
    source code. All the user has to do is open the Cold Calling app by, for
    example, double clicking on the icon. If the user wishes to run the software
    through the source code, use python3 to open GUI/HOME.py.

    If this is the first time using the software, the user will need to first import
    a roster. this can be accomplished by either selecting the button "Input a Roster"
    or "User View" to select the class roster. Otherwise, click on "User View" to open
    a window that selects four student to be called on.

    Note that the summary performance file and daily log file are different
    between running our source code directly and running the app. They do not use
    the same two files, so running, for example, the source code will generate
    log files that are completely separate from the ones found in the app.

    Refer to the user guide for more detailed instructions on how to use our
    software.

Documentation:
	Documentation regarding the project may be found in the documentation folder. This 	includes a System Design Specification, System Requirements Specification, as well 	as a User and Programmer Documentation.

Requirements
    Requires Python 3.3 to 3.7 and a Mac computer running a modern version of macOS.
    The software was developed and tested on macOS 10.14 (Mojave)
