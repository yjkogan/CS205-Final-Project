#import necessary modules
import sys
import random as rand
import comparisons as scr

# import MRJob class
from mrjob.job import MRJob
from collections import defaultdict

#Hard coded teacher list. Updated dynamically by wrapper python script
teacherlist = ["38","Jason","MA","11/9/2008 20:41,8043176","662","7231","Grove Hall Prep Middle School","Math | Number Sense and Operations | Algebra | Geometry | Data Analysis and Probability | Measurement","RPC 6th Grade Math Procedures | RPC 6th Grade Math Problem Solving | GHP 5th Grade Math Y","1 Whole Numbers | 2 Decimals | 3 Fractions | 4 Percents | 5 Geometry | Daily Activities | 6 Extensions and Review | Assessments | Whole Numbers | Integers | Number Theory | Data Analysis | Ratio and Proportion | Linear Relationships | Fractions | Decimals | Percents | Probability | Expressions | Patterns and Sequences | Measurement | Volume | Perimeter and Area | Working with Data | Coordinate Plane | Polygons | 3D Geometry | Introduction to Math Y","Fifth grade",'','','','','','','']

#Hard coded dictionary associating columns with their numeric values
coldict = {'SchoolName':7,'State':2,'Grades':11}

#Function to calculate the similarity score
def get_score(teacher,tocompare):
    #keeps track of the contributions of each characteristic
    scoredict = {}
    #keeps track of the total score
    scoreval =0
    #keeps track of the number of meaningful comparisons
    num_cats_compared = 0
    #iterates through the different columns we want to compare
    for c,v in coldict.iteritems():
        if(c == 'SchoolName'):
            score = scr.compSchool(teacher[v],tocompare[v])
            #If a meaningful comparison happened, update the score trackers
            if(score != None):
                scoredict[c]=score
                scoreval += score
                num_cats_compared += 1
        if(c == 'State'):
            score = scr.compState(teacher[v],tocompare[v])
            if(score != None):
                scoredict[c]=score
                scoreval += score
                num_cats_compared += 1
        if(c == 'Grades'):
            score = scr.compGrades(teacher[v],tocompare[v])
            if(score != None):
                scoredict[c]=score
                scoreval += score
                num_cats_compared += 1

    '''Taken from http://desk.stinkpot.org:8080/tricks/index.php/2006/10/... 
    find-the-key-for-the-minimum-or-maximum-value-in-a-python-dictionary/'''
    #Inverts the dictionary (swaps keys and values) so that we can get the max value
    temp = dict(map(lambda scores: (scores[1],scores[0]),scoredict.items()))
    #Gets the largest contributor to score. Ties are broken arbitrarily
    try:
        largestcontributor = temp[max(temp)]
    except ValueError:
        largestcontributor = None
    
    #Returns a tuple of the score and the number of meaningful comparisons that happened
    return (round(scoreval,5),num_cats_compared)

class MyWordCount(MRJob):
    def __init__(self,*args,**kwargs):
        super(MyWordCount,self).__init__(*args,**kwargs)
        #List to keep track of the teachers we have compared
        self.comparedts = []
        #The teacher we are comparing
        self.teacher = teacherlist
    # override pre-defined mapper by creating a generator
    # with the default name (mapper)
    def mapper(self, key, value):
        #Need this so that mr.job thinks it is a generator
        if 0:
            yield
        row = value.split(',')
        #calculate the score
        score = get_score(self.teacher,row)
        #Add this score to the list of teachers. If no meaningful comparisons happened, add 0
        try:
            self.comparedts.append((row[:3],score[0]/score[1]))
        except ZeroDivisionError:
            self.comparedts.append((row[:3],0))

    def mapper_final(self):
        #yield the top ten most similar teachers
        yield None, sorted(self.comparedts,\
                               key=(lambda x: x[1]),reverse=True)[:10]

    # override pre-defined reducer by creating a generator
    # with the default name (reducer)
    def reducer(self, key, values):
        allcompared = []
        for value in values:
            allcompared.extend(value)
        yield key, sorted(allcompared,key=(lambda x: x[1]),reverse=True)[:10]


if __name__ == '__main__':
    # launch the job!
#    mr_job = MyWordCount(args=[filename,])
    mr_job = MyWordCount()
    mr_job.run()


# Combiner instead of mapper_final
# Less computationally intensive mappers
# More computationally intensive
