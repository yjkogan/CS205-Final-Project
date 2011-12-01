import argparse,os

#Sets the directory for the where the defaults are stored
defaults_directory = 'defaults/'

#creates the string for the path to the default columns fileXS
def_col_path = os.path.join(defaults_directory,'defaultcolumns.txt')

#Creates a parser object
parser = argparse.ArgumentParser(description = \
                                    "Parser for similarity score launcher")

'''determines what arguments the parser should look for
any argument without a '-' symbol is required, any argument with a '-' symbol
is optional and correctly sets that variable to the next command line argument.
The 'defaults' argument sets what the default should be if no argument is
provided'.
'''

#Argument for the map-reduce script we want to run
parser.add_argument('scripttorun')
#Argument for the csv file where all our data is stored
parser.add_argument('database')
#File where we can find a dictionary relating fields and column number
parser.add_argument('-c','--columnsfile',default=def_col_path)
#File where we can find the teacher we are comparing
parser.add_argument('teacher')
#If -d or --debug is on the command line, turn on debug mode
parser.add_argument('-d','--debug',action='store_true',default=False)
#If -emr is given then run the script on amazon
parser.add_argument('-emr',action='store_true',default=False)
