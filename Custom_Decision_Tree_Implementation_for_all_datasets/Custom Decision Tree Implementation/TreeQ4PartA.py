import math
import random
from random import randint
from collections import Counter

def readData(file):
    data = [[]]
    for line in file:
        data.append([w.lower() for w in line.strip("\r\n").split(',')])
    data.remove([])
    return data
def GetaccuracyPercentage(test_data, classifications):
    correct = 0
    for x in range(len(test_data)):
        if str(test_data[x]) == str(classifications[x]):
            correct += 1
    return (correct/float(len(test_data))) * 100.0
class Tree:
    value = ""
    child = []

    def __init__(self, val, dictionary):
        self.setVal(val)
        self.getchild(dictionary)

    def __str__(self):
        return str(self.value)

    def setVal(self, val):
        self.value = val

    def getchild(self, dictionary):
        if(isinstance(dictionary, dict)):
            self.child = dictionary.keys()

class treebuilder:
    def search(self,item, list):
        for i in list:
            if item(i):
                return True
            else:
                return False

    #get most frequent value for a column attribute
    def getmostfrequentvalue(self,attributes, dataset, classAttributename):
        Frequency = {}
        classind = attributes.index(classAttributename)
        for tuple in dataset:
            if (Frequency.has_key(tuple[classind])):
                Frequency[tuple[classind]] += 1
            else:
                Frequency[tuple[classind]] = 1
        return max(Frequency, key=Frequency.get)
    def getEntropy(self,attributes, dataset, classAttributename):
        EntropyVal = 0.0
        Frequency = {}
        i = 0
        for item in attributes:
            if (classAttributename == item):
                break
            ++i
        for item in dataset:
            if (Frequency.has_key(item[i])):
                Frequency[item[i]] += 1.0
            else:
                Frequency[item[i]]  = 1.0
        for freqitem in Frequency.values():
            EntropyVal += (-freqitem/len(dataset)) * math.log(freqitem/len(dataset), 2)
        return EntropyVal

    def gini(self,attributes, dataset, classAttributename):

        Frequency = {}
        ginival = 0.0
        i = 0
        for item in attributes:
            if (classAttributename == item):
                break
            ++i
        for item in dataset:
            if (Frequency.has_key(item[i])):
                Frequency[item[i]] += 1.0
            else:
                Frequency[item[i]]  = 1.0
        for freq in Frequency.values():
            ginival += ((freq/len(dataset)) ** 2)
        return 1-ginival

    def calculateInformationGain(self,attributes, dataset, attr, classAttributename):
        Frequency = {}
        entropymid = 0.0
        i = attributes.index(attr)
        for item in dataset:
            if (Frequency.has_key(item[i])):
                Frequency[item[i]] += 1.0
            else:
                Frequency[item[i]]  = 1.0
        for val in Frequency.keys():
            valProb = Frequency[val] / sum(Frequency.values())
            subdata = [item for item in dataset if item[i] == val]
            entropymid += valProb * self.gini(attributes, subdata, classAttributename)
        return (self.gini(attributes, dataset, classAttributename) - entropymid)

    #choose best attibute
    def getmostlikelyAttribute(self,dataset, attributes, classAttributename):
        best = attributes[0]
        maxGain = 0;
        for attr in attributes:
            newGain = self.calculateInformationGain(attributes, dataset, attr, classAttributename)
            if newGain>maxGain:
                maxGain = newGain
                best = attr
        return best

    #get values in the column of the given attribute
    def getColumnValues(self,dataset, attributes, attr):
        index = attributes.index(attr)
        values = []
        for item in dataset:
            if item[index] not in values:
                values.append(item[index])
        return values

    def samples(self,dataset, attributes, best, val):
        sample = [[]]
        index = attributes.index(best)
        for item in dataset:
            if (item[index] == val):
                newVal = []
                for i in range(0,len(item)):
                    if(i != index):
                        newVal.append(item[i])
                sample.append(newVal)
        sample.remove([])
        return sample

    def buildDecisionTree(self,dataset, attributes, classAttributename, numRecursions):
        dataset = dataset[:]
        numRecursions =numRecursions+ 1
        vals = [record[attributes.index(classAttributename)] for record in dataset]
        default = self.getmostfrequentvalue(attributes, dataset, classAttributename)
        if not dataset or (len(attributes) - 1) <= 0:
            return default
        elif vals.count(vals[0]) == len(vals):
            return vals[0]
        else:
            best = self.getmostlikelyAttribute(dataset, attributes, classAttributename)
            tree = {best:{}}
            for val in self.getColumnValues(dataset, attributes, best):
                examples = self.samples(dataset, attributes, best, val)
                newAttr = attributes[:]
                newAttr.remove(best)
                subtree = self.buildDecisionTree(examples, newAttr, classAttributename, numRecursions)
                tree[best][val] = subtree

        return tree

    
if __name__ == '__main__':
    """
    Training Data
    """
    givenclassValues=[]
    predictedList=[]
    filetrain = open('iris.datatrain.csv')
    print '\nTraining the model.......'
    classAttributename = "class"
    data=readData(filetrain)
    classindex=data[0].index('class')
    attributes = data[0]
    data.remove(attributes)
    random.shuffle(data)
    x=len(data)
    trainindex=int(0.9*x)
    testindex=int(0.1*x)
    train_data = data[:trainindex]
    test_data = data[-testindex:]
    tree = treebuilder().buildDecisionTree(train_data, attributes, classAttributename, 0)
    print "\n------------------------Final Decision tree----------------"
    print str(tree)
    #Testing the data
    print '\nTesting the data.......\n'
    for i in xrange(0,len(test_data)):
        givenclassValues.append(test_data[i][classindex])
    for item in test_data:
        dictree = tree.copy()
        result = ""
        while(isinstance(dictree, dict)):
            root = Tree(dictree.keys()[0], dictree[dictree.keys()[0]])
            dictree = dictree[dictree.keys()[0]]
            index = attributes.index(root.value)
            value = item[index]
            if(value in dictree.keys()):
                child = Tree(value, dictree[value])
                result = dictree[value]
                dictree = dictree[value]
            else:
                result = list(set(givenclassValues))[randint(0,set(givenclassValues).__len__()-1)]
                break
        predictedList.append(result)
    for i in range(0,len(predictedList)):
        print('Given Class =' + str(givenclassValues[i]) + ', Predicted Class =' + str(predictedList[i]))
    percentagecorrect = GetaccuracyPercentage(givenclassValues, predictedList)
    print('\nPercentage of class values predicted correctly' +' -->'+ str(percentagecorrect) + '%\n')