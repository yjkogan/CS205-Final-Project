#################################################################################
########################################Start Comparisons.py####################
import difflib as d

# Comparison functions. Return 1 for match, 0 for no match
# Returns a float between 0 and 1 based on similarity for fuzzy matching (eg subject material)

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
# takes two strings that are lists using | as demarcator and checks if any element in string1 is in string2
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
# takes two strings that are lists using | as demarcator and checks if any element in string1 is in string2
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
# returns 1 if string1 is "similar enough" to string2 using difflib with precision precis
def compFuzzy(string1, string2, precis):
	# if string is not provided, do not return a score
	if (string1 == '\N' or string2 == '\N'):
		return None

	# not using literal comparison, using difflib to catch mispellings
	else:
		# try quick_ratio() if this is too slow.
		if (d.SequenceMatcher(None, string1, string2).ratio() > precis):
			# SHOULD be same school; might have to play with comparison value
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
#Updated dynamically by wrapper python script 'mr_launcher.py'
teacherlist = ["38","Jason","MA","11/9/2008 20:41","8043176","662","7231","Grove Hall Prep Middle School","Math | Number Sense and Operations | Algebra | Geometry | Data Analysis and Probability | Measurement","RPC 6th Grade Math Procedures | RPC 6th Grade Math Problem Solving | GHP 5th Grade Math Y","1 Whole Numbers | 2 Decimals | 3 Fractions | 4 Percents | 5 Geometry | Daily Activities | 6 Extensions and Review | Assessments | Whole Numbers | Integers | Number Theory | Data Analysis | Ratio and Proportion | Linear Relationships | Fractions | Decimals | Percents | Probability | Expressions | Patterns and Sequences | Measurement | Volume | Perimeter and Area | Working with Data | Coordinate Plane | Polygons | 3D Geometry | Introduction to Math Y","Fifth grade",'','','','','','','']


#Placeholder for the coldict variable.
#Updated dynamically by wrapper python script 'mr_launcher.py'
coldict = {'SchoolName':7,'State':2,'Grades':11,'TeacherID':0,'TeacherName':1,'DateCreated':3,'Score':4,'Uploads':5,'Downloads':6,'Subjects':8,'Courses':9,'Units':10}


#Function to calculate the similarity score
def get_score(teacher,tocompare):
    c = tocompare[0]
    valtocomp = tocompare[1]
    v = coldict[c]
    #keeps track of the total score
    scoreval = 0
    #keeps track of the number of meaningful comparisons
    num_cats_compared = 0
    #iterates through the different columns we want to compare
    if(c == 'SchoolName'):
        score = compSchool(teacher[v],valtocomp)
        #If a meaningful comparison happened, update the score trackers
        if(score != None):
            scoreval += score
            num_cats_compared += 1
    elif(c == 'State'):
        score = compState(teacher[v],valtocomp)
        if(score != None):
            scoreval += score
            num_cats_compared += 1
    elif(c == 'Grades'):
        score = compGrades(teacher[v],valtocomp)
        if(score != None):
            scoreval += score
            num_cats_compared += 1
    elif(c == 'Subjects'):
        score = compGrades(teacher[v],valtocomp)
        if(score != None):
            scoreval += score
            num_cats_compared += 1
    elif(c == 'Units'):
        score = compGrades(teacher[v],valtocomp)
        if(score != None):
            scoreval += score
            num_cats_compared += 1
    elif(c == 'Courses'):
        score = compGrades(teacher[v],valtocomp)
        if(score != None):
            scoreval += score
            num_cats_compared += 1
    else:
        return None

    #Returns a tuple of the score and the number of meaningful comparisons
    return (round(scoreval,5),num_cats_compared)

class MyWordCount(MRJob):
    def __init__(self,*args,**kwargs):
        super(MyWordCount,self).__init__(*args,**kwargs)
        #List to keep track of the teachers we have compared
        self.scores = defaultdict(list)
        self.numcompared = defaultdict(int)
        #The teacher we are comparing
        self.teacher = teacherlist
    # override pre-defined mapper by creating a generator
    # with the default name (mapper)
    def mapper(self, key, value):
        #Need this so that mr.job thinks it is a generator
        if 0:
            yield
        row = map(lambda x: x.strip('\r'),value.split(','))
        id = int(row[0])
        #calculate the score
        score = get_score(self.teacher,row[1:])
        #Add this score to the list of teachers.
#        if id == 38 and score[0] == 0. and score[1]==1:
        if(score != None):
            self.scores[id].append((score[0],row[1]))
            self.numcompared[id]+=score[1]

    def mapper_final(self):
        #yield the top ten most similar teachers
        for id,scores in self.scores.iteritems():
            def add(a,b):
                return a+b[0]
            score = reduce(add,scores,0)
            largest_contributor =  max(scores)[1]
            if score != 0:
                yield id,(score/self.numcompared[id],largest_contributor)

    # override pre-defined reducer by creating a generator
    # with the default name (reducer)
    def reducer(self, key, values):
        totalscore = 0
        lrgst_contribs = []
        for score in values:
            totalscore += score[0]
            lrgst_contribs.append((score[0],score[1]))
        yield key,(totalscore,max(lrgst_contribs)[1])

if __name__ == '__main__':
    # launch the job!
#    mr_job = MyWordCount(args=[filename,])
    mr_job = MyWordCount()
    mr_job.run()


# Combiner instead of mapper_final
# Less computationally intensive mappers
# More computationally intensive
