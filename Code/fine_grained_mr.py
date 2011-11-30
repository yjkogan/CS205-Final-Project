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

#Function to calculate the similarity score
def get_score(teacher,tocompare):
    c = tocompare[0]
    valtocomp = tocompare[1]
    v = coldict[c]
    #keeps track of the total score
    scoreval = 0
    #keeps track of the number of meaningful comparisons
    num_cats_compared = 0
    #iterates through the different columns we want to compare
    if(c == 'SchoolName'):
        score = scr.compSchool(teacher[v],valtocomp)
        #If a meaningful comparison happened, update the score trackers
        if(score != None):
            scoreval += score
            num_cats_compared += 1
    if(c == 'State'):
        score = scr.compState(teacher[v],valtocomp)
        if(score != None):
            scoreval += score
            num_cats_compared += 1
    if(c == 'Grades'):
        score = scr.compGrades(teacher[v],valtocomp)
        if(score != None):
            scoreval += score
            num_cats_compared += 1

    #Returns a tuple of the score and the number of meaningful comparisons
    return (round(scoreval,5),num_cats_compared)

class MyWordCount(MRJob):
    def __init__(self,*args,**kwargs):
        super(MyWordCount,self).__init__(*args,**kwargs)
        #List to keep track of the teachers we have compared
        self.scores = defaultdict(list)
        self.numcompared = defaultdict(int)
        #The teacher we are comparing
        self.teacher = teacherlist
    # override pre-defined mapper by creating a generator
    # with the default name (mapper)
    def mapper(self, key, value):
        #Need this so that mr.job thinks it is a generator
        if 0:
            yield
        row = map(lambda x: x.strip('\r'),value.split(','))
        id = int(row[0])
        #calculate the score
        score = get_score(self.teacher,row[1:])
        #Add this score to the list of teachers.
#        if id == 38 and score[0] == 0. and score[1]==1:
        self.scores[id].append((score[0],row[1]))
        self.numcompared[id]+=score[1]

    def mapper_final(self):
        #yield the top ten most similar teachers
        for id,scores in self.scores.iteritems():
            def add(a,b):
                return a+b[0]
            score = reduce(add,scores,0)
            largest_contributor =  max(scores)[1]
            if score != 0:
                yield id,(score/self.numcompared[id],largest_contributor)

    # override pre-defined reducer by creating a generator
    # with the default name (reducer)
    def reducer(self, key, values):
        totalscore = 0
        lrgst_contribs = []
        for score in values:
            totalscore += score[0]
            lrgst_contribs.append((score[0],score[1]))
        yield key,(totalscore,max(lrgst_contribs)[1])

if __name__ == '__main__':
    # launch the job!
#    mr_job = MyWordCount(args=[filename,])
    mr_job = MyWordCount()
    mr_job.run()


# Combiner instead of mapper_final
# Less computationally intensive mappers
# More computationally intensive
