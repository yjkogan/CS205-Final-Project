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
provided'
'''
parser.add_argument('scripttorun')
parser.add_argument('database')
parser.add_argument('-c','--columnsfile',default=def_col_path)
parser.add_argument('teacher')
