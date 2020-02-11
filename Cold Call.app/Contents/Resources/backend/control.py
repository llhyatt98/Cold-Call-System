'''
algorithm for how to pick a fair and random queue.

with in a reasonable size of class, greater or equal 5, this algorithm will guarantee
    * random: you can't predict who will be next
    * fair: the different of the chance been called between each student is less than 0.01
    * cool down time: student will not been called continuously. The bigger size for ROster, the longer cool down time there will be

To test or run only this file:
    1. comment out line 19 (from backend.objects import Student, classQueue)
    2. uncommen line 18 (# from objects import Student, classQueue)
    3. python3 control.py

Author: Yin Jin 
'''


# from objects import Student, classQueue
from backend.objects import Student, classQueue
import random
# https://www.programiz.com/python-programming/datetime/current-datetime
from datetime import date


# only first N% in the quene may be deck, N ->(30-50)
N = 45

def N_index(length):
    index = 0 
    if length < 12:
        index = 5
    else:
        index = int(length * N / 100) - 1
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
    # victimStudent.numCalled += 1
    Roster.enqueue(victimStudent)
    # 
    onDeck.enqueue(victimStudent)
    return victimStudent

def initRoster():
    # init a Roster which is a quene of a Student objects 
    Roster = classQueue()
    
    # delet later
    # replace with a function later
    student1 = Student("Lucas", "Hyatt", 951550079, "llh@uoregon.edu", "loo-kiss", True, 0, 0, [])
    student2 = Student("Maura", "McCabe", 111222333, "maura@uoregon.edu", "mor-uh", True, 0, 0, [])
    student3 = Student("Noah", "Tigner", 123456789, "notig@uoregon.edu", "no-uh", False, 0, 0, [])
    student4 = Student("Jimmy", "Lam", 987654321, "jim@uoregon.edu", "ji-mee", True, 0, 0, [])
    student5 = Student("Yin", "Jin", 123789456, "yjin@uoregon.edu", "yi-n", False, 0, 0, [])
    student6 = Student("Anthony", "Hornoff", 123456789, "noff@uoregon.edu", "hor-noff", True, 0, 0, [])

    student7 = Student("Ann", "Hyatt", 951550076, "llh@uoregon.edu", "loo-kiss", True, 0, 0, [])
    student8 = Student("Nation", "McCabe", 111222336, "maura@uoregon.edu", "mor-uh", True, 0, 0, [])
    student9 = Student("Jessie", "Tigner", 123456786, "notig@uoregon.edu", "no-uh", False, 0, 0, [])
    student10= Student("Harry", "Lam", 987654326, "jim@uoregon.edu", "ji-mee", True, 0, 0, [])
    student11 = Student("Haihan", "Jin", 123789455, "yjin@uoregon.edu", "yi-n", False, 0, 0, [])
    student12 = Student("Quan", "Hornoff", 123456786, "noff@uoregon.edu", "hor-noff", True, 0, 0, [])
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
    return Roster

def initDeck(Roster):
    # given a Roster, 
    # return onDeck Quene: 4 student object
    onDeck = classQueue()

    for i in range(4):
        pickOneStudent(onDeck, Roster)

    return onDeck


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

    # update the imformation for picked student 
    for sd in Roster.queue:
        if (sd.uoID == student.uoID):
            sd.numCalled += 1
            sd.dates.append(date.today().strftime("%d/%m/%y"))
            sd.numFlags += 1
            sd.reveal = 1
            flagQ.enqueue(sd)
            break;

    onDeck.removeIndex(cur_index)
    pickOneStudent(onDeck, Roster)

    # reset the current_index to 0
    return 0

def down(cur_index, onDeck, Roster):
    # remove one student that been picked
    student = onDeck.removeIndex(cur_index)
    # update the imformation for picked student 
    isFind = 0
    for sd in Roster.queue:
        if (sd.uoID == student.uoID):
            sd.numCalled += 1
            sd.dates.append(date.today().strftime("%d/%m/%y"))
            isFind = 1
            break;
    pickOneStudent(onDeck, Roster)

    # print("IsFind:", isFind==1, "!!!!!!!!!!!")

    # print("IN control")
    # for i in range(Roster.length):
    #     print("Queue at index", i, "has", end = " ")
    #     sd = Roster.queue[i]
        # print(sd.fname, sd.numCalled, sd.numFlags, sd.dates)
    return 0

def OnDeckString(cur_index, onDeck):
    # formate four name
    # return the information of day to day mode that update() in GUI need 

    if (onDeck.length != 4):
        print("Error: not enough student on Deck")
        return 0

    # inText = "Next students:"
    inText = " "


    for i in range(4):
        student = onDeck.queue[i]
        name = "  " + student.fname + " " + student.lname

        if (i == cur_index):
            highlightStart = len(inText) + 2
            highlightEnd = len(inText) + len(name)

        inText += name

    return inText, highlightStart, highlightEnd

def importFun():
    # used for testing import file
    print("!!!!!!!!!!!!!!!!!!")
    print("sucessfuly import file control")

def testRandomness():

    # init all the imformation
    Roster = initRoster()

    # 4 student object on deck, current_Index will be the index
    onDeck = initDeck(Roster)

    total = 10000
    for i in range(total):
        current_Index = down(0, onDeck, Roster)

    print("\n\n############ Report ###################\n\n")
    li = []
    for i in range(Roster.length):
        print("Queue at index", i, "has", end = " ")
        sd = Roster.queue[i]
        li.append(sd.numCalled/total)
        print(sd.fname, sd.numCalled, "chance been called: ", sd.numCalled / total)


    print("\nRange for chance been called:", round(max(li) - min(li), 4), "\n")

def main():

    testRandomness()


#     # init all the imformation
#     Roster = initRoster()

#     # # 4 student object on deck, current_Index will be the index 
#     onDeck = initDeck(Roster)

#     # the picked student's index in onDeck queue
#     current_Index = 0

#     # a list of student been flag
#     flagQ = classQueue()

#     # print(OnDeckString(current_Index, onDeck))



#     print("\n\n############ sucessfuly import!! ###################\n\n")

#     # onDeck = initDeck(Roster)
#     print(OnDeckString(current_Index, onDeck))

#     # 1
#     # current_Index = right(current_Index, onDeck, Roster)
#     # print(OnDeckString(current_Index, onDeck))

#     # 0
#     # current_Index = left(current_Index, onDeck, Roster)
#     # # 3
#     # current_Index = left(current_Index, onDeck, Roster)
#     # # 2
#     # current_Index = left(current_Index, onDeck, Roster)
#     # # 1
#     # current_Index = left(current_Index, onDeck, Roster)

#     # print(OnDeckString(current_Index, onDeck))

#     current_Index = up(current_Index, onDeck, Roster, flagQ)
#     print(OnDeckString(current_Index, onDeck))
#     flagQ.printQ()

#     # current_Index = right(current_Index, onDeck, Roster)
#     # print(OnDeckString(current_Index, onDeck))

#     current_Index = down(current_Index, onDeck, Roster)
#     print(OnDeckString(current_Index, onDeck))


#     # Roster.printQ()
#     for i in range(Roster.length):
#         print("Queue at index", i, "has", end = " ")
#         sd = Roster.queue[i]
#         print(sd.fname, sd.numCalled, sd.numFlags, sd.reveal)


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
