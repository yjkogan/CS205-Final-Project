################################################################################
########################################Start Comparisons.py####################
import difflib as d

# Comparison functions. Return 1 for match, 0 for no match
# Returns a float between 0 and 1 based on similarity for fuzzy 
# matching (eg subject material)

# Since the goal of this assignment was to explore how to make parallel
# algorithms more efficient these similarity scores are very rudimentary

# compares similarity of schools
def compSchool(string1, string2):
	return compFuzzy(string1, string2, .8)
			
# compares state
def compState(string1, string2):
	return compVerbatim(string1, string2)

# compare grades
def compGrades(string1, string2):
	return compList(string1, string2)

# compare subjects
def compSubjects(string1, string2):
	return compList(string1, string2)

# compare units
def compUnits(string1, string2):
	# make this less shit, needs to be smarter
	return compFuzzyList(string1, string2, .4)

# compare courses
def compCourses(string1, string2):
	# make this less shit, needs to be smarter
	return compFuzzyList(string1, string2, .4)


# converts string of strings w delimiter, strips and lowercases list of strings
def prepStringList(string, delim):
	list = string.split(delim)
	return map((lambda x: x.strip().lower()),list)

# string list membership check
# takes two strings that are lists using | as demarcator and 
# checks if any element in string1 is in string2
def compList(string1, string2):
	# if strings not provided, do not return a score
	if (string1 == '\N' or string2 == '\N'):
		return None
	
	# array of strings, lowercased and no whitespace
	list1 = prepStringList(string1, '|')
	list2 = prepStringList(string2, '|')
	
	# make this less shit: not binary, faster?
	for i in list1:
		if i in list2:
			return 1
	return 0

# string list membership check that is fuzzy
# takes two strings that are lists using | as demarcator 
# and checks if any element in string1 is in string2
def compFuzzyList(string1, string2, precis):
	# if strings not provided, do not return a score
	if (string1 == '\N' or string2 == '\N'):
		return None
	
	# array of strings, lowercased and no whitespace
	list1 = prepStringList(string1, '|')
	list2 = prepStringList(string2, '|')
	
	# make this less shit: not binary, parallelize!
	for i in list1:
		for j in list2:
			if (compFuzzy(i,j, precis)):
				return 1
	return 0

# fuzzy string comparison
# returns 1 if string1 is "similar enough" 
# to string2 using difflib with precision precis
def compFuzzy(string1, string2, precis):
	# if string is not provided, do not return a score
	if (string1 == '\N' or string2 == '\N'):
		return None

	# not using literal comparison, using difflib to catch mispellings
	else:
                #These are "toy" comparisons
		if (d.SequenceMatcher(None, string1, string2).ratio() > precis):
			return 1
		else:
			# different school
			return 0

# compares two strings verbatim
def compVerbatim(string1, string2):
	# if a string is not provided, do not return a score
	if (string1 == '\N' or string2 == '\N'):
		return None
	elif (string1.lower() == string2.lower()):
		# same
		return 1
	else:
		# different
		return 0
########################################End Comparsions.py######################
################################################################################

#import necessary modules
import sys
import random as rand

# import MRJob class
from mrjob.job import MRJob
from collections import defaultdict

#Placeholder for the teacherlist variable.
#Updated dynamically by wrapper python script 'mr_launcher2.py'
#teacherlist_placeholder#

#Dictionary of the the column number associated with each field
coldict={'SchoolName':7,'State':2,'Grades':11,'TeacherID':0,'TeacherName':1,\
'DateCreated':3,'Score':4,'Uploads':5,'Downloads':6,'Subjects':8,'Courses':9,\
                 'Units':10}

#Dictionary so that we can find the correct function simply from
#the name of the field
funcs = {'SchoolName':compSchool,'State':compState,'Grades':compGrades,\
'Subjects':compSubjects,'Courses':compCourses,'Units':compUnits}

def get_score(teacher,tocompare):
    #keeps track of the contributions of each characteristic
    scoredict = {}
    #keeps track of the total score
    scoreval =0
    #keeps track of the number of meaningful comparisons
    num_cats_compared = 0
    #iterates through the different columns we want to compare
    for c,v in coldict.iteritems():
       score = None
       if c in funcs:
          score = funcs[c](teacher[v],tocompare[v])
       #If a meaningful comparison happened, update the score trackers
       if(score != None):
          scoredict[c]=score
          scoreval += score
          num_cats_compared += 1

    #Returns a tuple of the score and the number of meaningful comparisons
    return (round(scoreval,5),num_cats_compared)

class MySimTeachers(MRJob):
    def __init__(self,*args,**kwargs):
        super(MySimTeachers,self).__init__(*args,**kwargs)
        #List to keep track of the teachers we have compared
        self.comparedts = []
        #The teacher we are comparing
        self.teacher = teacherlist
    # override pre-defined mapper by creating a generator
    # with the default name (mapper)
    def mapper(self, key, value):
        #Need this so that mr.job thinks it is a generator
        if 0:
            yield
        row = value.split(',')
        #calculate the score for teachers with higher IDs only
	if (self.teacher[0] >= row[0]):
		return
	score = get_score(self.teacher,row)
	#Add this score to the list of teachers.
        #If no meaningful comparisons happened, add nothing
        try:
            self.comparedts.append((int(row[0]),score[0]/score[1]))
        except ZeroDivisionError,ValueError:
            pass
    
    def mapper_final(self):
        # yield the top ten most similar teachers
        # The score is the 1 value in the tuple, so make that the key
        # Then sort so that the front of the list is the most common teachers
        # Only pass the top 10 because a) we aren't going to use more than that
        # and b) because it is very costly on the map-reduce framework to pass
        # lots of data
        yield None, sorted(self.comparedts,\
                               key=(lambda x: x[1]),reverse=True)[:10]

    # override pre-defined reducer by creating a generator
    # with the default name (reducer)
    def reducer(self, key, values):
        # Accumulate all the most similar teachers in one list and select
        # The top 10 of them
        allcompared = []
        for value in values:
            allcompared.extend(value)
        yield key, sorted(allcompared,key=(lambda x: x[1]),reverse=True)[:10]


if __name__ == '__main__':
    # launch the job!
    mr_job = MySimTeachers()
    mr_job.run()

