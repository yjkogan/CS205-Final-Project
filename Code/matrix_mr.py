#import necessary modules
import sys
import random as rand
import comparisons as scr

# import MRJob class
from mrjob.job import MRJob
from collections import defaultdict

#Placeholder for the teacherlist variable.
#Updated dynamically by wrapper python script 'mr_launcher.py'
#teacherlist_placeholder#

#Placeholder for the coldict variable.
#Updated dynamically by wrapper python script 'mr_launcher.py'
#coldict_placeholder#

#Placeholder for the filename variable.
#Updated dynamically by wrapper python script 'mr_launcher.py'
#filename_placeholder#

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
        elif(c == 'State'):
            score = scr.compState(teacher[v],tocompare[v])
            if(score != None):
                scoredict[c]=score
                scoreval += score
                num_cats_compared += 1
        elif(c == 'Grades'):
            score = scr.compGrades(teacher[v],tocompare[v])
            if(score != None):
                scoredict[c]=score
                scoreval += score
                num_cats_compared += 1
        elif(c == 'Subjects'):
            score = scr.compGrades(teacher[v],tocompare[v])
            if(score != None):
                scoredict[c]=score
                scoreval += score
                num_cats_compared += 1
        elif(c == 'Courses'):
            score = scr.compGrades(teacher[v],tocompare[v])
            if(score != None):
                scoredict[c]=score
                scoreval += score
                num_cats_compared += 1
        elif(c == 'Units'):
            score = scr.compGrades(teacher[v],tocompare[v])
            if(score != None):
                scoredict[c]=score
                scoreval += score
                num_cats_compared += 1

    '''Taken from http://desk.stinkpot.org:8080/tricks/index.php/2006/10/ 
    find-the-key-for-the-minimum-or-maximum-value-in-a-python-dictionary/'''
    #Inverts the dictionary (swaps keys and values) so that we can 
    #get the max value
    temp = dict(map(lambda scores: (scores[1],scores[0]),scoredict.items()))
    #Gets the largest contributor to score. Ties are broken arbitrarily
    try:
        largestcontributor = temp[max(temp)]
    except ValueError:
        largestcontributor = None
    
    #Returns a tuple of the score and the number of meaningful comparisons
    
    return (round(scoreval,5),num_cats_compared)

class MySimTeachers(MRJob):
    def __init__(self,*args,**kwargs):
        super(MySimTeachers,self).__init__(*args,**kwargs)
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
        #Add this score to the list of teachers.
        #If no meaningful comparisons happened, add 0
        try:
            self.comparedts.append((int(row[0]),score[0]/score[1]))
        except ZeroDivisionError:
            self.comparedts.append((int(row[0]),0))
        except ValueError:
            pass

    def mapper_final(self):
        #yield the top ten most similar teachers
        yield None, sorted(self.comparedts,\
                               key=(lambda x: x[1]),reverse=True)

    # override pre-defined reducer by creating a generator
    # with the default name (reducer)
    def reducer(self, key, values):
        allcompared = []
        for value in values:
            allcompared.extend(value)
        yield key, sorted(allcompared,key=(lambda x: x[1]),reverse=True)


if __name__ == '__main__':
    # launch the job!
#    mr_job = MySimTeachers(args=[filename,])
    mr_job = MySimTeachers()
    mr_job.run()


# Combiner instead of mapper_final
# Less computationally intensive mappers
# More computationally intensive
