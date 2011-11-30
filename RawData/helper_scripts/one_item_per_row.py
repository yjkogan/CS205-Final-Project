import csv,sys,os,ast
default_columns_location = '../../Code/defaults/defaultcolumns.txt'
try:
   datafile = sys.argv[1]
except IndexError:
   print "Not enough command line arguments"
   exit(0)
datatoreshape= sys.argv[1]

print "Reshaping " + datatoreshape + '\n'

file = open(default_columns_location,'r')
coldict = ast.literal_eval(file.read())
file.close()

outlocation = '../reshaped/reshaped_finegrained_mapper_user_export.csv'

writer = csv.writer(\
   open(outlocation,'w'))

reader = csv.reader(open(datatoreshape,'r'))

i = 0
for row in reader:
   if i > 0:
      id = row[int(coldict['TeacherID'])]
      for c,v in coldict.iteritems():
         writer.writerow([id,(c,row[v])])
   else:
      i +=1

print 'Wrote file ' + outlocation + "\n"
