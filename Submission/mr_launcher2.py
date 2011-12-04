import subprocess,time,sys,csv
import string as st
from myparser import parser
import re
import time

# parse the command line arguments
args = parser.parse_args()

# read dataset
file = open(args.scripttorun,'r')
filetext =  file.read()
file.close()
inputfile = csv.reader(open(args.inputfile,'r'))
scoreDict = {}

# for debugging
counter = 0
RUNCOUNT = 20
start = time.time()

# takes two strings, and write text to file named filename, with mode mode
def logStuff(filename, text, mode):
	log = open(filename, mode)
	log.write(text)
	log.close()

# iterate over every row in the csv
for row in inputfile:
	#Fill in teacherlist variable
	currentID = eval(row[0])
	teacherstring = 'teacherlist = ' + str(row)
	tempfiletext = st.replace(filetext,'#teacherlist_placeholder#',\
                                          teacherstring)

	#Create a temporary script to run using the new script we 
        #have dynamically generated.
	print "Creating temporary script file tempscript.py\n"
	tempfile = open('tempscript.py','w')
	tempfile.write(tempfiletext)
	tempfile.close()

	#run the map_reduce job

	#If debugging mode is on, just run the mapper
	#Do this because it makes print statements (in the mapper) work
	if(args.debug):
	   proc = subprocess.Popen(['python','tempscript.py',args.database,\
                                            '--mapper'],stdout=subprocess.PIPE)
        elif(args.emr):
           #If the -emr flag is given, then this script runs
           #The given script (repeatedly) on emr.
	   proc = subprocess.Popen(['python','tempscript.py',args.database,\
                                            '-r','emr','--jobconf',\
                                            #Change this value to launch
                                            #more mapper jobs
                                            'mapred.map.tasks=4'],\
                                           stdout=subprocess.PIPE)
	else:
           proc = subprocess.Popen(['python','tempscript.py',args.database],\
                                           stdout=subprocess.PIPE)

        while True:
		# this bit of code reads from tempscript's stoud
		line = proc.stdout.readline()
		if line != '':
                        # gets the list of comparisons from stdout w regex
			result = eval(re.search('\\t(.*)\\n',line).group(0)) 
			for k,v in result: # k,v is teacherID, score
                                # makes sorted tuple of the currentID and the
                                #ID being compared to to use as key
				keyTuple = tuple(sorted([k,currentID])) 
				if (keyTuple not in scoreDict):
					scoreDict[keyTuple] = v # set new score
                        print scoreDict
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
print 'It took {0} seconds to build the dictionary for {1} teachers.'.format(\
        runtime, RUNCOUNT)
print 'The average runtime per teacher was {0} seconds'.format(runtime/RUNCOUNT)
# logStuff('scoreDict.txt', str(scoreDict),'w')
# writes teachers run, agg runtime, avg runtime, and current time as a csv
logStuff('perfLog.csv', str(RUNCOUNT) + ',' + str(runtime) + ',' + \
                 str(runtime/RUNCOUNT) + ',' + time.strftime('%X %x %Z') \
                 +'\n', 'a')
