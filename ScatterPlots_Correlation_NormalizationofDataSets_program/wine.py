import scipy
from scipy import stats
import matplotlib.pyplot as bplot
import operator
from operator import itemgetter
import scipy.spatial.distance as d
from scipy import stats

Alcohol=[]
MalicAcid=[]
Ash=[]
Alcalinity=[]
Magnesium=[]
phenols=[]
Flavanoids=[]
Nonflavanoid=[]
Proanthocyanins=[]
ColorIntensity=[]
Hue=[]
dilutedwines=[]
Proline=[]
rowdata=[]
classlist=[]
predictedclass=[]
corrdict={}
featureslist=['Alcohol','MalicAcid','Ash','Alcalinity','Magnesium','phenols','Flavanoids','Nonflavanoid','Proanthocyanins','ColorIntensity','Hue','dilutedwines','Proline']
def read_data(fname):

    file = open(fname, 'r');
    for line in file:
        dataline = [w.lower() for w in line.split(',')]
        Alcohol.append(float(dataline[1].strip()))
        MalicAcid.append(float(dataline[2]))
        Ash.append(float(dataline[3].strip()))
        Alcalinity.append(float(dataline[4].strip()))
        Magnesium.append(float(dataline[5].strip()))
        phenols.append(float(dataline[6]))
        Flavanoids.append(float(dataline[7]))
        Nonflavanoid.append(float(dataline[8]))
        Proanthocyanins.append(float(dataline[9]))
        ColorIntensity.append(float(dataline[10]))
        Hue.append(float(dataline[11]))
        dilutedwines.append(float(dataline[12]))
        Proline.append(float(dataline[13]))
        rowdata.append([float(i) for i in dataline[-13:]])
        classlist.append(dataline[0])


def read_data01normal(fname):
    global Alcohol,MalicAcid,Ash,Alcalinity,Magnesium,phenols,Flavanoids,Nonflavanoid,Proanthocyanins,ColorIntensity,Hue,dilutedwines,Proline
    file = open(fname, 'r');
    for line in file:
        dataline = [w.lower() for w in line.split(',')]
        Alcohol.append(float(dataline[1].strip()))
        MalicAcid.append(float(dataline[2]))
        Ash.append(float(dataline[3].strip()))
        Alcalinity.append(float(dataline[4].strip()))
        Magnesium.append(float(dataline[5].strip()))
        phenols.append(float(dataline[6]))
        Flavanoids.append(float(dataline[7]))
        Nonflavanoid.append(float(dataline[8]))
        Proanthocyanins.append(float(dataline[9]))
        ColorIntensity.append(float(dataline[10]))
        Hue.append(float(dataline[11]))
        dilutedwines.append(float(dataline[12]))
        Proline.append(float(dataline[13]))
        classlist.append(dataline[0])
    Alcohol = [round(float(i)/sum(Alcohol),2) for i in Alcohol]
    MalicAcid = [round(float(i)/sum(MalicAcid),2) for i in MalicAcid]
    Ash = [round(float(i)/sum(Ash),2) for i in Ash]
    Alcalinity = [round(float(i)/sum(Alcalinity),2) for i in Alcalinity]
    Magnesium = [round(float(i)/sum(Magnesium),2) for i in Magnesium]
    phenols = [round(float(i)/sum(phenols),2) for i in phenols]
    Flavanoids = [round(float(i)/sum(Flavanoids),2) for i in Flavanoids]
    Nonflavanoid = [round(float(i)/sum(Nonflavanoid),2) for i in Nonflavanoid]
    Proanthocyanins = [round(float(i)/sum(Proanthocyanins),2) for i in Proanthocyanins]
    ColorIntensity = [round(float(i)/sum(ColorIntensity),2) for i in ColorIntensity]
    Hue = [round(float(i)/sum(Hue),2) for i in Hue]
    dilutedwines = [round(float(i)/sum(dilutedwines),2) for i in dilutedwines]
    Proline = [round(float(i)/sum(Proline),2) for i in Proline]
    for i in range(len(Alcohol)):
        rowdata.append([Alcohol[i],MalicAcid[i],Ash[i],Alcalinity[i],Magnesium[i],phenols[i],Flavanoids[i],Nonflavanoid[i],Proanthocyanins[i],ColorIntensity[i],Hue[i],dilutedwines[i],Proline[i]])

def read_datazscore(fname):
    global Alcohol,MalicAcid,Ash,Alcalinity,Magnesium,phenols,Flavanoids,Nonflavanoid,Proanthocyanins,ColorIntensity,Hue,dilutedwines,Proline
    file = open(fname, 'r');
    for line in file:
        dataline = [w.lower() for w in line.split(',')]
        Alcohol.append(float(dataline[1].strip()))
        MalicAcid.append(float(dataline[2]))
        Ash.append(float(dataline[3].strip()))
        Alcalinity.append(float(dataline[4].strip()))
        Magnesium.append(float(dataline[5].strip()))
        phenols.append(float(dataline[6]))
        Flavanoids.append(float(dataline[7]))
        Nonflavanoid.append(float(dataline[8]))
        Proanthocyanins.append(float(dataline[9]))
        ColorIntensity.append(float(dataline[10]))
        Hue.append(float(dataline[11]))
        dilutedwines.append(float(dataline[12]))
        Proline.append(float(dataline[13]))
        classlist.append(dataline[0])
    Alcohol = stats.zscore(Alcohol)
    MalicAcid = stats.zscore(Alcohol)
    Ash = stats.zscore(Alcohol)
    Alcalinity = stats.zscore(Alcohol)
    Magnesium = stats.zscore(Alcohol)
    phenols = stats.zscore(Alcohol)
    Flavanoids = stats.zscore(Alcohol)
    Nonflavanoid = stats.zscore(Alcohol)
    Proanthocyanins = stats.zscore(Alcohol)
    ColorIntensity = stats.zscore(Alcohol)
    Hue =stats.zscore(Alcohol)
    dilutedwines = stats.zscore(Alcohol)
    Proline = stats.zscore(Alcohol)
    for i in range(len(Alcohol)):
        rowdata.append([Alcohol[i],MalicAcid[i],Ash[i],Alcalinity[i],Magnesium[i],phenols[i],Flavanoids[i],Nonflavanoid[i],Proanthocyanins[i],ColorIntensity[i],Hue[i],dilutedwines[i],Proline[i]])



def plotscatter(max):
    for i in range(0,len(max)):
        bplot.scatter(eval(max[i].split(',')[0]),eval(max[i].split(',')[1]))
        bplot.ylabel('<---------------------'+ max[i].split(',')[1] + '------------------------>')
        bplot.xlabel('<------------------------'+ max[i].split(',')[0] + '------------------------------------>')
        bplot.show()

def GetaccuracyPercentage(test_data, classifications):
	correct = 0
	for x in range(len(test_data)):
		if test_data[x] == classifications[x]:
			correct += 1
	return (correct/float(len(test_data))) * 100.0

def getclosestNeighborClass(trainingdata, testdata):
    ListDistances = []
    for i in range(0,len(trainingdata)):
        distance = d.euclidean(testdata, trainingdata[i])
        ListDistances.append(distance)
    m = min(k for k in ListDistances if k > 0)
    return classlist[ListDistances.index(m)]

if __name__== "__main__":
    trainfile='wine.data'
    read_data(trainfile)
    for i in range(0,len(featureslist)-1):
        for j in range(i+1,len(featureslist)):
            corrdict[featureslist[i]+","+featureslist[j]]=[abs(scipy.stats.pearsonr(eval(featureslist[i]),eval(featureslist[j]))[0])]
    print corrdict
    listsortedkeys=[]
    for key in sorted(corrdict.iteritems(), key=itemgetter(1), reverse=True):
        listsortedkeys.append(key[0])
    maxlist=listsortedkeys[:4]
    plotscatter(maxlist)
    minlist=listsortedkeys[-4:]
    plotscatter(minlist)
    for i in range(0,len(rowdata)):
        pclass=getclosestNeighborClass(rowdata,rowdata[i])
        predictedclass.append(pclass)
        print('Predicted Class =' + pclass + ', Original Class =' + str(classlist[i])+ '\n')

    percentagecorrect=GetaccuracyPercentage(predictedclass, classlist)
    print('\nPercentage of points correctly classified in dataset as a whole' +' -->'+ str(percentagecorrect) + '%\n')
    plist1,plist2,plist3,clist1,clist2,clist3=([] for i in range(6))
    for i in range(0,len(classlist)):
        if classlist[i]=='1':
            plist1.append(predictedclass[i])
            clist1.append(classlist[i])
        if classlist[i]=='2':
            plist2.append(predictedclass[i])
            clist2.append(classlist[i])
        if classlist[i]=='3':
            plist3.append(predictedclass[i])
            clist3.append(classlist[i])

    percentagecorrect1=GetaccuracyPercentage(plist1, clist1)
    print('\nPercentage of points correctly classified for Class 1' +' -->'+ str(percentagecorrect1) + '%\n')
    percentagecorrect2=GetaccuracyPercentage(plist2, clist2)
    print('\nPercentage of points correctly classified for Class 2' +' -->'+ str(percentagecorrect2) + '%\n')
    percentagecorrect3=GetaccuracyPercentage(plist3, clist3)
    print('\nPercentage of points correctly classified for Class 3' +' -->'+ str(percentagecorrect3) + '%\n')