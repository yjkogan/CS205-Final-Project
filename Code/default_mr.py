#import necessary modules
import sys

# import MRJob class
from mrjob.job import MRJob
from collections import defaultdict

inputfile = "../RawData/betterlesson.hcs_user_export.csv"

class MyWordCount(MRJob):
    def __init__(self,*args,**kwargs):
        super(MyWordCount,self).__init__(*args,**kwargs)
        self.letters = defaultdict(list)
    # override pre-defined mapper by creating a generator
    # with the default name (mapper)
    def mapper(self, key, value):
        yield self.teacher[0],self.teacher[1:]

    # override pre-defined reducer by creating a generator
    # with the default name (reducer)
    def reducer(self, key, values):
        yield key, values


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
