'''
Initialization of Objects used within the System
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




