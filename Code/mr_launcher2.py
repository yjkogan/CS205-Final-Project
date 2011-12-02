import subprocess,time,sys,csv
import string as st
from myparser import parser
import re
import time

#parse the command line arguments
args = parser.parse_args()

'''The next several lines of code take the script we want to run and
fill in the variables teacherlist and coldict using the data stored
in the files provided on the command line. To do this, it does a string
replacement on specific placeholder strings in the script, in particular
'#teacherlist_placeholder#' and '#coldict_placeholder#'.'''

comparisons = open("comparisons.py",'r')
filetext = comparisons.read()
comparisons.close()        

file = open(args.scripttorun,'r')
filetext +=  file.read()
file.close()
database = csv.reader(open(args.database,'r'))
scoreDict = {}

start = time.time()

# for debugging
counter = 0
RUNCOUNT = 2

# does logging stuff
def logStuff(filename, text):
	log = open(filename,'a')
	log.write(text)
	log.close()

for row in database:
	#Fill in teacherlist variable
	currentID = eval(row[0])
	teacherstring = 'teacherlist = ' + str(row)
	tempfiletext = st.replace(filetext,'#teacherlist_placeholder#',teacherstring)

	#Fill in the coldict variable
	columns = open(args.columnsfile,'r')
	colstring = 'coldict = ' + columns.read()
	tempfiletext = st.replace(tempfiletext,'#coldict_placeholder#',colstring)
        filenamestring = 'filename = \"' + args.database + "\""
        tempfiletext = st.replace(tempfiletext,'#filename_placeholder#',\
                                          filenamestring)


	#Create a temporary script to run using the new script we have dynamically
	#generated.
	print "Creating temporary script file tempscript.py\n"
	tempfile = open('tempscript.py','w')
	tempfile.write(tempfiletext)
	tempfile.close()

	#run the map_reduce job

	#If debugging mode is on, just run the mapper
	#Do this because it makes print statements (in the mapper) work
	if(args.debug):
	   proc = subprocess.Popen(['python','tempscript.py',args.database,'--mapper'],stdout=subprocess.PIPE)
	else:
           #proc = subprocess.Popen(['python','tempscript.py'],stdout=subprocess.PIPE)
<<<<<<< HEAD
	   proc = subprocess.Popen(['python','tempscript.py',args.database,'-r','emr'],stdout=subprocess.PIPE)
=======
	   proc = subprocess.Popen(['python','tempscript.py',args.database],stdout=subprocess.PIPE)
	   # proc = subprocess.Popen(['python','tempscript.py',args.database,'-r','emr'],stdout=subprocess.PIPE)
>>>>>>> 0c5af223d404bd9ae25916220063e1759f02be5a
           while True:
		line = proc.stdout.readline()
		if line != '':
			result = eval(re.search('\\t(.*)\\n',line).group(0)) # gets the list of comparison from stdout
			for k,v in result: # k,v is teacherID, score
				keyTuple = tuple(sorted([k,currentID])) # makes sorted tuple of the currentID and the ID being compared to to use as key
				if (keyTuple not in scoreDict):
					scoreDict[keyTuple] = v
			# print scoreDict
		else:
			break

	print "Cleaning up..."
	print "    Removing tempscript.py"
	subprocess.call(['rm','tempscript.py'])
	counter += 1
	if (counter == RUNCOUNT):
		break

runtime = time.time() - start
print 'It took {0} seconds to build the dictionary for {1} teachers.'.format(runtime, RUNCOUNT)
print 'The average runtime per teacher was {0} seconds'.format(runtime/RUNCOUNT)
# logStuff('scoreDict.txt', str(scoreDict))
logStuff('perfLog.csv', str(RUNCOUNT) + ',' + str(runtime) + ',' + str(runtime/RUNCOUNT) + ',' + time.strftime('%X %x %Z') +'\n') # writes teachers run, agg runtime, and avg runtime as a csv, and current time
