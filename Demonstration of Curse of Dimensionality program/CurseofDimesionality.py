import numpy as np
import matplotlib.pyplot as plt
import math
listofpoints=[]
dictfinalvalues={}
def CalculateEuclideanDistance(set1, set2):
	distance = 0
	for x in range(0,len(set1)):
		distance += (set1[x] - set2[x])**2
	return distance


def CalculateDMaxMin(a):
    distanceslist=[]
    for i in range(0,len(a)):
        for j in range(i+1,len(a)):
            distanceslist.append(CalculateEuclideanDistance(a[i],a[j]))
    dmax = max(distanceslist)
    dmin = min(distanceslist)
    return dmax,dmin



if __name__== "__main__":
    for k in xrange(1,101):
        listofpoints= np.random.uniform(0,1,size=(100,k))
        dmax,dmin=CalculateDMaxMin(listofpoints)
        finalresult=math.log((dmax-dmin)/dmin,10)
        dictfinalvalues[k]=finalresult
        print k,dictfinalvalues[k]


