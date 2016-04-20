import random
import math
import collections
from collections import defaultdict
import numpy as np
import itertools
import operator
from random import randint
import os
#import scipy.spatial.distance as d
#d.euclidean()
#d.cityblock()
#d.chebyshev()
class Recommender:
    def __init__(self):
        self.UserMovieDict={}
        self.MovieUserDict={}
        self.MovieRating={}
        self.UserRatingDict={}
        self.UserDict={}
        self.MovieDict={}
        self.distancefromNeighbors={}
        self.distancepreviousneighbors={}
        self.predictedRating=[]
        self.givenRating=[]
    def GetaccuracyPercentage(self,test_data, classifications):
        correct = 0
        for x in range(len(test_data)):
            if str(test_data[x]) == str(classifications[x]):
                correct += 1
        return (correct/float(len(test_data))) * 100.0
    def GetMADvalue(self,test_data, classifications):
        correct = 0
        differenceList=[]
        for x in range(len(test_data)):
            differenceList.append((math.fabs(float(test_data[x])-float(classifications[x]))-1)*10)
        return (sum(differenceList)/float(len(test_data)))

    def CalculateEuclideanDistance(self,set1, set2):
        distance = 0
        for x in range(0,len(set1)):
            distance += (set1[x] - set2[x])**2
        return math.sqrt(distance)
    def CalculateManhattanDistance(self,set1, set2):
        distance = 0
        for x in range(0,len(set1)):
            distance += abs(set1[x] - set2[x])
        return distance
    def CalculateLmaxDistance(self,set1, set2):
        distance = []
        for x in range(0,len(set1)):
            distance.append(abs(set1[x] - set2[x]))
        if not distance:
            return 0
        else:
            return max(distance)
    def getMaximumLikelyOrientation(self,neighbors):
        neighborOrientation = {}
        for x in range(len(neighbors)):
            orientation = neighbors[x]
        if orientation in neighborOrientation:
           neighborOrientation[orientation] += 1
        else:
           neighborOrientation[orientation] = 1
        sortedOrientation= sorted(neighborOrientation.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sortedOrientation[0][0]
    def read_data(fname):
        datafinal = []
        file = open(fname, 'r');
        for line in file:
            dataline = [w.lower() for w in line.split()]
            datafinal.append(dataline)
        return datafinal

    def train(self, datafile, moviefile, userfile, occupationfile,distancemetric,algo):
        file = open(datafile, 'r');
        for line in file:
            dataline = [w.lower() for w in line.split()]
            if (dataline[1] in self.MovieRating):
                self.MovieRating[dataline[1]].append(int(dataline[2]))
            else:
                self.MovieRating[dataline[1]]= [int(dataline[2])]
        file.close()
        file = open(datafile, 'r');
        for line in file:
            dataline = [w.lower() for w in line.split()]
            if (dataline[0] in self.UserMovieDict):
                self.UserMovieDict[dataline[0]].append(dataline[1])
            else:
                self.UserMovieDict[dataline[0]] = [dataline[1]]

            if (dataline[0] in self.UserRatingDict):
                self.UserRatingDict[dataline[0]].append(int(dataline[2]))
            else:
                self.UserRatingDict[dataline[0]]= [int(dataline[2])]

            if (dataline[1] in self.MovieUserDict):
                self.MovieUserDict[dataline[1]].append(dataline[0])
            else:
                self.MovieUserDict[dataline[1]]=  [dataline[0]]
        if algo=='parta':

           #Calculate how many movies user has not seen
            for i in xrange(1,self.UserMovieDict.__len__()+1):
                for j in xrange(i+1,self.UserMovieDict.__len__()+1):
                    Ratingsbyi=[]
                    Ratingsbyj=[]
                    #find common movies between user i,j
                    commonlist=list(set(self.UserMovieDict[str(i)]) & set(self.UserMovieDict[str(j)]))
                    for k in xrange(0,len(commonlist)):
                        Ratingsbyi.append(self.UserRatingDict[str(i)][self.UserMovieDict[str(i)].index(commonlist[k])])
                        Ratingsbyj.append(self.UserRatingDict[str(j)][self.UserMovieDict[str(j)].index(commonlist[k])])
                    #distance calculation:
                    if distancemetric=='euclidean':
                        if (str(i) in self.distancefromNeighbors):
                            self.distancefromNeighbors[str(i)].append(self.CalculateEuclideanDistance(Ratingsbyi,Ratingsbyj))
                        else:
                            self.distancefromNeighbors[str(i)]=[self.CalculateEuclideanDistance(Ratingsbyi,Ratingsbyj)]
                    elif distancemetric=='manhattan':
                        if (str(i) in self.distancefromNeighbors):
                            self.distancefromNeighbors[str(i)].append(self.CalculateManhattanDistance(Ratingsbyi,Ratingsbyj))
                        else:
                            self.distancefromNeighbors[str(i)]=[self.CalculateManhattanDistance(Ratingsbyi,Ratingsbyj)]
                    elif distancemetric=='lmax':
                        if (str(i) in self.distancefromNeighbors):
                            self.distancefromNeighbors[str(i)].append(self.CalculateLmaxDistance(Ratingsbyi,Ratingsbyj))
                        else:
                            self.distancefromNeighbors[str(i)]=[self.CalculateLmaxDistance(Ratingsbyi,Ratingsbyj)]
                    del Ratingsbyi[:]
                    del Ratingsbyj[:]
                    del commonlist[:]
            for i in xrange(2,self.UserMovieDict.__len__()+1):
                for j in xrange(1,i):
                    if (str(i) in self.distancepreviousneighbors):
                        self.distancepreviousneighbors[str(i)].append(self.distancefromNeighbors[str(j)][(i-j)-1])
                    else:
                        self.distancepreviousneighbors[str(i)] = [self.distancefromNeighbors[str(j)][(i-j)-1]]
        else:
            file = open(userfile, 'r');
            for line in file:
                dataline = [w.lower() for w in line.split('|')]
                if dataline[2]=='m':
                    x=1
                else:
                    x=0

                if (dataline[0] in self.UserDict):
                    self.UserDict[dataline[0]].append(int(dataline[1]))
                else:
                    self.UserDict[dataline[0]]= [int(dataline[1])]
                self.UserDict[dataline[0]].append(int(x))
            file.close()
           #Calculate how many movies user has not seen
            for i in xrange(1,self.UserMovieDict.__len__()+1):
                for j in xrange(i+1,self.UserMovieDict.__len__()+1):
                    Ratingsbyi=[]
                    Ratingsbyj=[]
                    #find common movies between user i,j
                    commonlist=list(set(self.UserMovieDict[str(i)]) & set(self.UserMovieDict[str(j)]))
                    for k in xrange(0,len(commonlist)):
                        Ratingsbyi.append(self.UserRatingDict[str(i)][self.UserMovieDict[str(i)].index(commonlist[k])])
                        Ratingsbyj.append(self.UserRatingDict[str(j)][self.UserMovieDict[str(j)].index(commonlist[k])])
                    #distance calculation:
                    if distancemetric=='euclidean':
                        if (str(i) in self.distancefromNeighbors):
                            self.distancefromNeighbors[str(i)].append(self.CalculateEuclideanDistance(Ratingsbyi+self.UserDict[str(i)],Ratingsbyj+self.UserDict[str(j)]))
                        else:
                            self.distancefromNeighbors[str(i)]=[self.CalculateEuclideanDistance(Ratingsbyi+self.UserDict[str(i)],Ratingsbyj+self.UserDict[str(j)])]
                    elif distancemetric=='manhattan':
                        if (str(i) in self.distancefromNeighbors):
                            self.distancefromNeighbors[str(i)].append(self.CalculateManhattanDistance(Ratingsbyi+self.UserDict[str(i)],Ratingsbyj+self.UserDict[str(j)]))
                        else:
                            self.distancefromNeighbors[str(i)]=[self.CalculateManhattanDistance(Ratingsbyi+self.UserDict[str(i)],Ratingsbyj+self.UserDict[str(j)])]
                    elif distancemetric=='lmax':
                        if (str(i) in self.distancefromNeighbors):
                            self.distancefromNeighbors[str(i)].append(self.CalculateLmaxDistance(Ratingsbyi+self.UserDict[str(i)],Ratingsbyj+self.UserDict[str(j)]))
                        else:
                            self.distancefromNeighbors[str(i)]=[self.CalculateLmaxDistance(Ratingsbyi+self.UserDict[str(i)],Ratingsbyj+self.UserDict[str(j)])]
                    del Ratingsbyi[:]
                    del Ratingsbyj[:]
                    del commonlist[:]
            for i in xrange(2,self.UserMovieDict.__len__()+1):
                for j in xrange(1,i):
                    if (str(i) in self.distancepreviousneighbors):
                        self.distancepreviousneighbors[str(i)].append(self.distancefromNeighbors[str(j)][(i-j)-1])
                    else:
                        self.distancepreviousneighbors[str(i)] = [self.distancefromNeighbors[str(j)][(i-j)-1]]
#    def getKNeighbors(self, user, k):
#        ListDistances = []
#        for i in range(0,len(trainingdata)):
#            distance = calculateDistance(testdata, trainingdata[i])
#            ListDistances.append((trainingdata[i], distance))
#        neighbors = []
#        ListDistances.sort(key=operator.itemgetter(1))
#        for x in range(k):
#            neighbors.append(ListDistances[x][0])
#        return neighbors
    def predictRatings(self,testfile):
        file = open(testfile, 'r');
        for line in file:
            dataline = [w.lower() for w in line.split()]
            movie=dataline[1]
            rating=dataline[2]
            user=dataline[0]
            self.givenRating.append(rating)
            if user in self.distancefromNeighbors:
                neighbors1=self.distancefromNeighbors[user]
            else:
                neighbors1=[]
            if user=='1':
                neighbors2=[]
            else:
                neighbors2=self.distancepreviousneighbors[user]
            totalneighbors=neighbors2+neighbors1
            userlistaccordingtoneighbor=list(xrange(1,944))
            userlistaccordingtoneighbor.remove(int(user))
            minL = np.array(totalneighbors)
            q=list(minL.argsort()[:940][::-1])
            listmovieseenneighbor=[]
            for i in xrange(len(q)):
                if movie in self.MovieUserDict:
                    if str(userlistaccordingtoneighbor[q[i]]) in self.MovieUserDict[movie]:
                        listmovieseenneighbor.append(userlistaccordingtoneighbor[q[i]])

            if not listmovieseenneighbor or len(listmovieseenneighbor)<3:
                print ''
            else:
                x=0
                if len(listmovieseenneighbor)>40:
                    x=40
                elif len(listmovieseenneighbor)>20 and len(listmovieseenneighbor)<40:
                    x=39
                elif len(listmovieseenneighbor)<20 and len(listmovieseenneighbor)>10:
                    x=19
                else:
                    x=3
                Ratingsfinal=[]
                kneighbors=listmovieseenneighbor[:5]
                for i in range(len(kneighbors)):
                    if ((str(kneighbors[i]) in self.UserMovieDict) and (str(kneighbors[i]) in self.UserRatingDict)):
                        Ratingsfinal.append(self.UserRatingDict[str(kneighbors[i])][self.UserMovieDict[str(kneighbors[i])].index(movie)])
                    else:
                        if movie in self.MovieRating:
                            x=int(math.floor(np.mean(self.MovieRating[movie])))
                            Ratingsfinal.append(str(x))
                result = self.getMaximumLikelyOrientation(Ratingsfinal)
                if (result=='') or (result is None) or (not result):
                    if movie in self.MovieRating:
                        x= np.mean(self.MovieRating[movie])
                        self.predictedRating.append(x)
                        print('Original Rating =' + str(rating) + ', Predicted Rating =' + str(x))
                    else:
                        self.predictedRating.append('5')
                        print('Original Rating =' + str(rating) + ', Predicted Rating =' + str('5'))
                else:
                    self.predictedRating.append(result)
                    print('Original Rating =' + str(rating) + ', Predicted Rating =' + str(result))

            if len(self.givenRating)!=len(self.predictedRating):
                self.predictedRating.append(str(randint(3,5)))

            del Ratingsfinal[:]
            del neighbors2[:]
            del listmovieseenneighbor[:]
#        percentagecorrect=self.GetaccuracyPercentage(self.givenRating, self.predictedRating)
#        print('\nPercentage of movies rated correctly' +' -->'+ str(percentagecorrect) + '%\n')

        mad = self.GetMADvalue(self.givenRating, self.predictedRating)
        print('\nMean Absolute Difference(MAD) value is' +' -->'+ str(mad))

    def naive(self,testfile,datafile):
       file = open(datafile, 'r');
       for line in file:
            dataline = [w.lower() for w in line.split()]
            if (dataline[1] in self.MovieRating):
                self.MovieRating[dataline[1]].append(int(dataline[2]))
            else:
                self.MovieRating[dataline[1]]= [int(dataline[2])]
       file.close()
       file = open(testfile, 'r');
       Ratingsfinal=[]
       for line in file:
            dataline = [w.lower() for w in line.split()]
            movie=dataline[1]
            rating=dataline[2]
            user=dataline[0]
            self.givenRating.append(rating)
            if movie in self.MovieRating:
                x=int(math.floor(np.mean(self.MovieRating[movie])))
                Ratingsfinal.append(str(x))
            else:
                Ratingsfinal.append(str(randint(3,5)))
            result = self.getMaximumLikelyOrientation(Ratingsfinal)
            self.predictedRating.append(result)
            print('Original Rating =' + str(rating) + ', Predicted Rating =' + str(result))
            if len(self.givenRating)!=len(self.predictedRating):
                self.predictedRating.append(str(randint(3,5)))
            del Ratingsfinal[:]
       mad = self.GetMADvalue(self.givenRating, self.predictedRating)
       print('\nMean Absolute Difference(MAD) value is' +' -->'+ str(mad))
       percentagecorrect=self.GetaccuracyPercentage(self.givenRating, self.predictedRating)
       print('\nPercentage of movies rated correctly' +' -->'+ str(percentagecorrect) + '%\n')








if __name__== "__main__":
    print "Learning model..."
    datafile= os.path.join("/l/b565/","ml-100K/u1.base")
    testfile= os.path.join("/l/b565/","ml-100K/u1.test")
    moviefile=""
    userfile=""
    occupationfile=""
    recommender = Recommender()
    distancemetric='euclidean'
#   recommender.naive(testfile,datafile)
    algo='parta'
    recommender.train(datafile,moviefile,userfile,occupationfile,distancemetric,algo)
    recommender.predictRatings(testfile)