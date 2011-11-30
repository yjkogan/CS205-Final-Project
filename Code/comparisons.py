import difflib as d

# Comparison functions. Return 1 for match, 0 for no match

# compares similarity of schools
def compSchool(string1, string2):
	# if school is not provided, do not return a score
	if (string1 == '\N' or string2 == '\N'):
		return None
	# not using literal comparison, using difflib to catch mispellings
	else:
		# try quick_ratio() if this is too slow.
		if (d.SequenceMatcher(None, string1, string2).ratio() > .8):
			# SHOULD be same school; might have to play with comparison value
			return 1
		else:
			# different school
			return 0
			
# compares state
def compState(string1, string2):
	# if state is not provided, do not return a score
	if (string1 == '\N' or string2 == '\N'):
		return None
	elif (string1 == string2):
		# same state
		return 1
	else:
		# different state
		return 0

# compare courses
def compSubjects(string1, string2):
	# make this less shit, needs to be fuzzy
	return 1
	
# compare units
def compUnits(string1, string2):
	# make this less shit, needs to be fuzzy
	return 1
		
# compare grades
def compGrades(string1, string2):
	return compList(string1, string2)

# compare subjects
def compSubjects(string1, string2):
	return compList(string1, string2)

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
	
# takes string to list by delim, strips and lowercases list of strings
def prepStringList(string, delim):
	list = string.split(delim)
	return map((lambda x: x.strip().lower()),list)
		
