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

file = open(args.scripttorun,'r')
filetext =  file.read()
file.close()
inputfile = csv.reader(open(args.inputfile,'r'))
scoreDict = {}

start = time.time()

# for debugging
counter = 0
RUNCOUNT = 20

# does logging stuff
def logStuff(filename, text):
	log = open(filename,'a')
	log.write(text)
	log.close()

for row in inputfile:
	#Fill in teacherlist variable
	currentID = eval(row[0])
	teacherstring = 'teacherlist = ' + str(row)
	tempfiletext = st.replace(filetext,'#teacherlist_placeholder#',teacherstring)

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
           proc = subprocess.Popen(['python','tempscript.py',args.database],stdout=subprocess.PIPE)
	   #proc = subprocess.Popen(['python','tempscript.py',args.database,'-r','emr','--jobconf','mapred.map.tasks=4'],stdout=subprocess.PIPE)
           while True:
		line = proc.stdout.readline()
		if line != '':
			result = eval(re.search('\\t(.*)\\n',line).group(0)) # gets the list of comparison from stdout
			for k,v in result: # k,v is teacherID, score
				keyTuple = tuple(sorted([k,currentID])) # makes sorted tuple of the currentID and the ID being compared to to use as key
				if (keyTuple not in scoreDict):
					scoreDict[keyTuple] = v
                        #print scoreDict
		else:
			break

	print "Cleaning up..."
	print "    Removing tempscript.py"
	subprocess.call(['rm','tempscript.py'])
	counter += 1
        # print counter
        # byn = raw_input("Would you like to continue? (y/n)")
        # if(byn == 'n'):
        #         break
	if (counter == RUNCOUNT):
		break

runtime = time.time() - start
print 'It took {0} seconds to build the dictionary for {1} teachers.'.format(runtime, RUNCOUNT)
print 'The average runtime per teacher was {0} seconds'.format(runtime/RUNCOUNT)
# logStuff('scoreDict.txt', str(scoreDict))
logStuff('perfLog.csv', str(RUNCOUNT) + ',' + str(runtime) + ',' + str(runtime/RUNCOUNT) + ',' + time.strftime('%X %x %Z') +'\n') # writes teachers run, agg runtime, and avg runtime as a csv, and current time
