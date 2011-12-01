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
