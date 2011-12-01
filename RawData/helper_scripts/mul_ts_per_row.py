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

outlocation = '../reshaped/reshaped_coarsegrained_mapper_user_export.csv'

writer = csv.writer(\
   open(outlocation,'w'))

reader = csv.reader(open(datatoreshape,'r'))

i = -1
outrow = []
for row in reader:
   if i > -1:
      if((i % 5) !=4):
         outrow.append(row)
         i += 1
      else:
         outrow.append(row)
         outrow = zip(outrow[0],outrow[1],outrow[2],outrow[3],outrow[4])
         writer.writerow(outrow)
         outrow = []
         i += 1

   else:
      i +=1

print 'Wrote file ' + outlocation + "\n"
