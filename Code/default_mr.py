#import necessary modules
import sys
import random as rand

# import MRJob class
from mrjob.job import MRJob
from collections import defaultdict

teacherlist = ["38","Jason","MA","11/9/2008 20:41,8043176","662","7231","Grove Hall Prep Middle School","Math | Number Sense and Operations | Algebra | Geometry | Data Analysis and Probability | Measurement","RPC 6th Grade Math Procedures | RPC 6th Grade Math Problem Solving | GHP 5th Grade Math Y","1 Whole Numbers | 2 Decimals | 3 Fractions | 4 Percents | 5 Geometry | Daily Activities | 6 Extensions and Review | Assessments | Whole Numbers | Integers | Number Theory | Data Analysis | Ratio and Proportion | Linear Relationships | Fractions | Decimals | Percents | Probability | Expressions | Patterns and Sequences | Measurement | Volume | Perimeter and Area | Working with Data | Coordinate Plane | Polygons | 3D Geometry | Introduction to Math Y","Fifth grade",'','','','','','','']

def get_score(teacher,tocompare):
    return round(rand.random(),5)

class MyWordCount(MRJob):
    def __init__(self,*args,**kwargs):
        super(MyWordCount,self).__init__(*args,**kwargs)
        self.comparedts = []
        self.teacher = teacherlist
    # override pre-defined mapper by creating a generator
    # with the default name (mapper)
    def mapper(self, key, value):
        if 0:
            yield
        row = value.split(',')
        self.comparedts.append((row[:3],get_score(self.teacher[1:],row[1:])))

    def mapper_final(self):
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
    mr_job = MyWordCount()
    mr_job.run()









# # define new job by creating derived class
# class MyWordCount(MRJob):
#     def __init__(self,*args,**kwargs):
#         super(MyWordCount,self).__init__(*args,**kwargs)
#         self.letters = defaultdict(list)
#     # override pre-defined mapper by creating a generator
#     # with the default name (mapper)
#     def mapper(self, key, value):
#         if 0:
#             yield
#         self.letters["".join(sorted(value))].append(value)

#     def mapper_final(self):
#         for (letters2,words) in self.letters.iteritems():
#             yield letters2,words
    
#     # override pre-defined reducer by creating a generator
#     # with the default name (reducer)
#     def reducer(self, key, values):
#         allwords = []
#         for words in values:
#             allwords.extend(words)
#         yield key, (len(allwords),allwords)

# if __name__ == '__main__':
#     # launch the job!
#     MyWordCount.run()
