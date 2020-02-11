'''
Initialization of student and queue objects

Author: Lucas Hyatt
'''

class Student:
	def __init__(self, fname, lname, uoID, email, phoneticSpelling, revealCode, numCalled, numFlags, dates):
		self.fname = fname
		self.lname = lname
		self.uoID = uoID
		self.email = email
		self.phonetic = phoneticSpelling
		self.reveal = revealCode # Not entirely sure about this variable, just put it as boolean for now
		self.numCalled = numCalled # Number of times a student is called throughout the term
		self.flag = 0
		self.numFlags = numFlags
		self.dates = dates # List of dates when the student answered a question

	def printStudent(self):
		print("Student:", self.fname, self.lname, "has ID:", self.uoID)

	def display(self): # Will be called by UI, returns the name of student (Req 4.3)
		return self.fname + ' ' + self.lname

	def summaryPerformance(self): # Returns formatted string (Req. 3.D.3)
		# <total times called> <number of flags> <first name> <last name> <UO ID> <email address> <phonetic spelling> <reveal code><list of dates>
		return str(self.numCalled) + '\t' + str(self.numFlags) + '\t' + self.fname + '\t' + self.lname + '\t' + str(self.uoID) + '\t' + self.email + '\t' + self.phonetic + '\t' + str(self.reveal) + '\t' + str(self.dates) + '\n'

	def review(self): # Called by output file function feedback() (Req. 3.B.3)
		# <response_code> <tab> <first name> <last name> “<” <email address> “>” 
		return str(self.reveal) + '\t' + self.fname + ' ' + self.lname + ' <' + self.email + '>'

	def getFlag(self): #Helper to view the flag of a student
		return self.flag

	def setFlag(self, flag): #Helper to set the flag of a student
		self.flag = flag


# Testing

# student1 = Student("Lucas", "Hyatt", 951550079, "llh@uoregon.edu", "loo-kiss", True, 0, 0, [])
# student2 = Student("Maura", "McCabe", 111222333, "maura@uoregon.edu", "mor-uh", True, 0, 0, [])
# student3 = Student("Noah", "Tigner", 123456789, "notig@uoregon.edu", "no-uh", False, 0, 0, [])
# student4 = Student("Jimmy", "Lam", 987654321, "jim@uoregon.edu", "ji-mee", True, 0, 0, [])
# student5 = Student("Yin", "Jin", 123789456, "yjin@uoregon.edu", "yi-n", False, 0, 0, [])
# student6 = Student("Anthony", "Hornoff", 123456789, "noff@uoregon.edu", "hor-noff", True, 0, 0, [])
# print('Testing for student object: \n')
# student1.printStudent()
# print(student2.display())
# print(student3.summaryPerformance())
# print(student4.review())
# print('\n\n\n')

'''
Notes regarding input file (Source: https://classes.cs.uoregon.edu/20W/cis422/Handouts/Cold_Call_System_SRS_v2.pdf):

The UO ID will be nine digits.
The <reveal_code> will be used to indicate details about this entry, such as if the photo will be
displayed to other students in the classroom.
<LF> is a Unix line feed character.
The spaces around the <tab> and <LF> characters should not be added to the file. 

Line consists of:
<first_name> <tab> <last_name> <tab> <UO ID> <tab> <email_address> <tab> <phonetic_spelling> <tab> <reveal_code> <LF>
'''

class classQueue: 
	def __init__(self):
		self.queue = []
		self.length = 0

	def enqueue(self, new_student): #Enqueues new_student
		self.queue.append(new_student)
		self.length += 1

	def insertOne(self, new_student, i): # Inserts new_student at index i to The List
		self.queue.insert(i, new_student)
		self.length += 1

	def dequeue(self): #Removes oldest element from queue, returns the student upon success
		if self.length > 0:
			stud = self.queue.pop(0)
			self.length -= 1
			return stud
		print("Cannot dequeue, queue is empty...")

	def removeIndex(self, i):
		# Removes the student at index i from the list, returns removed student
		if self.length > 0:
			stud = self.queue.pop(i) #Removes at index i
			self.length -= 1
			return stud
		print("Cannot dequeue, queue is empty...")

	def isEmpty(self): # Checks whether an queue has any students
		if self.length == 0:
			return True
		return False

	def combine(self, new_list): #Combines a new list with the current queue (# Req: 3_C_1)
		self.length += len(new_list)
		self.queue += new_list

	def printQ(self):
		if len(self.queue) == 0:
			print("Nothing to print, queue is empty...")
		else:
			print("Length of queue is:", self.length)
			for i in range(self.length):
				print("Queue at index", i, "has", end = " ")
				self.queue[i].printStudent()



# print('Testing for queue object: \n')
# studentQ = classQueue()
# test = classQueue()
# test.enqueue(student1)
# test.enqueue(student2)
# test.enqueue(student3)
# test.enqueue(student4)
# test.enqueue(student5)
# test.enqueue(student6)

# studentQ.enqueue(student1)
# studentQ.enqueue(student2)
# studentQ.enqueue(student3)
# studentQ.enqueue(student4)
# studentQ.enqueue(student5)
# studentQ.enqueue(student6)

# studentQ.printQ()

# pop = studentQ.dequeue()
# pop.printStudent()
# studentQ.dequeue()
# studentQ.dequeue()

# studentQ.printQ()

# studentQ.dequeue()
# studentQ.printQ()
# studentQ.dequeue()
# studentQ.printQ()
# studentQ.dequeue()
# studentQ.printQ()
# studentQ.dequeue()

# print("Check for empty:", studentQ.isEmpty())
# studentQ.combine(test.queue)
# new_stud = Student("New", "Student", 951550079, "new@uoregon.edu", "yo-new", True, 0, 0, [])
# studentQ.insertOne(new_stud, 3)
# studentQ.printQ()
# print("Check for empty:", studentQ.isEmpty())



'''
Sources used: 

https://classes.cs.uoregon.edu/20W/cis422/Handouts/Cold_Call_System_SRS_v2.pdf
https://www.geeksforgeeks.org/queue-in-python/
'''




