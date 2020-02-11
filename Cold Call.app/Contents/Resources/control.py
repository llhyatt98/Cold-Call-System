from objects import Student, classQueue
import tkinter as tk
import time
import random

# only first N% in the quene may be deck, N ->(30-50)
N = 45

def N_index(length):
	index = int(length  * N / 100) - 1
	# print(index)

	return index

# N_index()

def pickOneStudent(onDeck,Roster):
    # change the Roster Quene and on Deck Quene,
    # return 0 if there is error, victimStudent if sucess.

    # error checking
    if onDeck.length > 4:
        print("Error: student on Deck already full")
        return 0

    n = N_index(Roster.length)

    # pick a student , place remove it from the original place and put it at the end
    index = random.randint(0,n);
    victimStudent = Roster.removeIndex(index)
    victimStudent.numCalled += 1
    Roster.enqueue(victimStudent)

    # 
    onDeck.enqueue(victimStudent)
    return victimStudent

def initDeck(onDeck, Roster):
    # initial four name
    for i in range(4):
        pickOneStudent(onDeck, Roster)

    return None


def left(cur_index, onDeck, Roster):
    cur_index = (cur_index -1 ) % 4
    return cur_index

def right(cur_index, onDeck, Roster):
    cur_index = (cur_index + 1) % 4
    return cur_index

def up(cur_index, onDeck, Roster, flagQ):
    # flag the student that picked (in current_Index)
    student = onDeck.queue[cur_index]
    # student.numFlags += 1
    for sd in Roster.queue:
        if (sd.uoID == student.uoID):
            sd.numFlags += 1

    onDeck.removeIndex(cur_index)
    sd = pickOneStudent(onDeck, Roster)
    flagQ.enqueue(sd)
    return 0

def down(cur_index, onDeck, Roster):
    # remove one student that been picked
    onDeck.removeIndex(cur_index)
    sd = pickOneStudent(onDeck, Roster)
    return 0

def OnDeckString(cur_index, onDeck):
    # formate four name
    # return the information of day to day mode that update() in GUI need 

    if (onDeck.length != 4):
        print("Error: not enough student on Deck")
        return 0

    inText = "Next students:"

    for i in range(4):
        student = onDeck.queue[i]
        name = "  " + student.fname + " " + student.lname

        if (i == cur_index):
            highlightStart = len(inText) + 2
            highlightEnd = len(inText) + len(name)

        inText += name

    return inText, highlightStart, highlightEnd



def main():
    # creat a golable Roster which is a quene of a Student object
    Roster = classQueue()

    # 4 student object on deck, current_Index will be the index 
    onDeck = classQueue()
    # the picked student's index in onDeck queue
    current_Index = 0

    # a list of student been flag
    flagQ = classQueue()


    # delet later
    # replace with a function later
    student1 = Student("Lucas", "Hyatt", 951550079, "llh@uoregon.edu", "loo-kiss", True, 0, 0, [])
    student2 = Student("Maura", "McCabe", 111222333, "maura@uoregon.edu", "mor-uh", True, 0, 0, [])
    student3 = Student("Noah", "Tigner", 123456789, "notig@uoregon.edu", "no-uh", False, 0, 0, [])
    student4 = Student("Jimmy", "Lam", 987654321, "jim@uoregon.edu", "ji-mee", True, 0, 0, [])
    student5 = Student("Yin", "Jin", 123789456, "yjin@uoregon.edu", "yi-n", False, 0, 0, [])
    student6 = Student("Anthony", "Hornoff", 123456789, "noff@uoregon.edu", "hor-noff", True, 0, 0, [])

    student7 = Student("Lucas1", "Hyatt", 951550076, "llh@uoregon.edu", "loo-kiss", True, 0, 0, [])
    student8 = Student("Maura1", "McCabe", 111222336, "maura@uoregon.edu", "mor-uh", True, 0, 0, [])
    student9 = Student("Noah1", "Tigner", 123456786, "notig@uoregon.edu", "no-uh", False, 0, 0, [])
    student10= Student("Jimmy1", "Lam", 987654326, "jim@uoregon.edu", "ji-mee", True, 0, 0, [])
    student11 = Student("Yin1", "Jin", 123789455, "yjin@uoregon.edu", "yi-n", False, 0, 0, [])
    student12 = Student("Anthony1", "Hornoff", 123456786, "noff@uoregon.edu", "hor-noff", True, 0, 0, [])
    Roster.enqueue(student1)
    Roster.enqueue(student2)
    Roster.enqueue(student3)
    Roster.enqueue(student4)
    Roster.enqueue(student5)
    Roster.enqueue(student6)
    Roster.enqueue(student7)
    Roster.enqueue(student8)
    Roster.enqueue(student9)
    Roster.enqueue(student10)
    Roster.enqueue(student11)
    Roster.enqueue(student12)


    print("\n\n############ sucessfuly import ###################\n\n")

    initDeck(onDeck,Roster)
    print(OnDeckString(current_Index, onDeck))

    # 1
    current_Index = right(current_Index, onDeck, Roster)
    print(OnDeckString(current_Index, onDeck))

    # 0
    current_Index = left(current_Index, onDeck, Roster)
    # 3
    current_Index = left(current_Index, onDeck, Roster)
    # 2
    current_Index = left(current_Index, onDeck, Roster)
    # 1
    current_Index = left(current_Index, onDeck, Roster)

    print(OnDeckString(current_Index, onDeck))

    current_Index = up(current_Index, onDeck, Roster, flagQ)
    print(OnDeckString(current_Index, onDeck))

    current_Index = right(current_Index, onDeck, Roster)
    # print(OnDeckString(current_Index, onDeck))

    current_Index = down(current_Index, onDeck, Roster)
    print(OnDeckString(current_Index, onDeck))


    # Roster.printQ()
    for i in range(Roster.length):
        print("Queue at index", i, "has", end = " ")
        sd = Roster.queue[i]
        print(sd.fname, sd.numCalled, sd.numFlags)


    # print("On Deck")
    # onDeck.printQ()
    # print(OnDeckString(current_Index, onDeck))
    # print()

	# Roster.printQ()
	# print(Roster.queue[3].fname)

    # name1 = "Maura McCabe"
    # name2 = "Jimmy Lam"
    # name3 = "Lucas Hyatt"
    # name4 = "Yin Jin"
    # name5 = 'Noah Tigner'

    # gui = GUI('Students on deck', 'green')

    # print('--- Starting GUI test ---')

    # names = "{}   {}   {}   {}".format(name1, name2, name3, name4)

    # highlightBegin = len(name1) + 3
    # highlightEnd = highlightBegin + len(name2)
    # gui.update(names, highlightBegin, highlightEnd)

    # # support for arrow key presses, bind() takes in function to use like pthread_create()

    # gui.mainWindow.bind("<Left>", gui.leftKey)
    # gui.mainWindow.bind("<Right>", gui.rightKey)
    # gui.mainWindow.bind("<Up>", gui.upKey)
    # gui.mainWindow.bind("<Down>", gui.downKey)

    # print("\033[38;5;220mClick on the cold call window. After pressing an arrow key,",
    # "\na message should be displayed. Close the cold call window to end the program.",
    # "\nNote: the names and highlighting should not update for this test.\033[0m")

    # gui.mainWindow.mainloop()  # blocks until the window is closed

if __name__ == '__main__':
    main()
