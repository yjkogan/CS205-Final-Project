'''
This script loads in the requested script (given as argument scripttorun)
and replaces some placeholders with information provided in other files.
This gives us a flexible way to change code by creating temporary files
with "hard-coded" values for the teacher we want to compare against the rest of
the database and for the column number of each field. The script
then creates a temporary file, runs it, and then removes that file.
'''


import subprocess,time,sys
import string as st
from myparser import parser

#parse the command line arguments
args = parser.parse_args()

'''The next several lines of code take the script we want to run and
fill in the variables teacherlist and coldict using the data stored
in the files provided on the command line. To do this, it does a string
replacement on specific placeholder strings in the script, in particular
'#teacherlist_placeholder#' and '#coldict_placeholder#'.'''
file = open(args.scripttorun,'r')
filetext =  file.read()

#Fill in teacherlist variable
teacher = open(args.teacher,'r')
teacherstring = 'teacherlist = ' + teacher.read()
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

start = time.time()
#run the map_reduce job

#If debugging mode is on, just run the mapper
#Do this because it makes print statements (in the mapper) work
if(args.debug):
   subprocess.call(['python','tempscript.py',args.database,'--mapper'])
elif(args.emr):
   subprocess.call(['python','tempscript.py','-r','emr',args.database,'--file=comparisons.pyc'])
else:
   subprocess.call(['python','tempscript.py',args.database])

print "It took %f seconds to run the map_reduce job" % (time.time() - start)

print "Cleaning up..."
print "    Removing tempscript.py"
#subprocess.call(['rm','tempscript.py'])
