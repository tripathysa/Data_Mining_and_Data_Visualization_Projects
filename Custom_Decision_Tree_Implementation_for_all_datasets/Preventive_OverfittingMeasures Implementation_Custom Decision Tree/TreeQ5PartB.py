
import math
import random
from random import randint
from collections import Counter
from collections import Counter
import matplotlib.pyplot as plt
validationset=[]
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
def performanceMeasure(truth, prediction):

    confusion_matrix = Counter()

    #say class 1, 3 are true; all other classes are false
    positives = [1,2,3,4]

    binary_truth = [x in positives for x in truth]
    binary_prediction = [x in positives for x in prediction]
    print binary_truth
    print binary_prediction

    for t, p in zip(binary_truth, binary_prediction):
        confusion_matrix[t,p] += 1

    print "TP: {} TN: {} FP: {} FN: {}".format(confusion_matrix[True,True], confusion_matrix[False,False], confusion_matrix[False,True], confusion_matrix[True,False])
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

    def __init__(self):
        self.errorslistperIteration=[]
        self.leveltraverse=0
        self.accuracyList=[]
    def search(self,item, list):
        for i in list:
            if item(i):
                return True
            else:
                return False

    #get most frequent value for a column attribute
    def getmostfrequentvalue(self,attributes, dataset, classAttributename):
        #find target attribute
        Frequency = {}
        #find target in data
        classind = attributes.index(classAttributename)
        #calculate frequency of values in target attr
        for tuple in dataset:
            if (Frequency.has_key(tuple[classind])):
                Frequency[tuple[classind]] += 1
            else:
                Frequency[tuple[classind]] = 1
        return max(Frequency, key=Frequency.get)
    def gini(self,attributes, dataset, classAttributename):

        Frequency = {}
        i = 0
        ginival = 0.0
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
        entropymid = 0.0
        Frequency = {}
        i = attributes.index(attr)
        for item in dataset:
            if (Frequency.has_key(item[i])):
                Frequency[item[i]] += 1.0
            else:
                Frequency[item[i]]  = 1.0
        for val in Frequency.keys():
            valProb= Frequency[val] / sum(Frequency.values())
            subData= [item for item in dataset if item[i] == val]
            entropymid += valProb * self.gini(attributes, subData, classAttributename)
        return (self.gini(attributes, dataset, classAttributename))

    #choose best attibute
    def getmostLikelyAttribute(self,dataset, attributes, classAttributename,validationset):
        best = attributes[0]
        maxVal= 0;
        for atrib in attributes:
            newVal = self.calculateInformationGain(attributes, dataset, atrib, classAttributename)
            if newVal>maxVal:
                maxVal = newVal
                best = atrib
        return best


    #get values in the column of the given attribute
    def getcolumnValues(self,dataset, attributes, attr):
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
                newEntry = []
                for i in range(0,len(item)):
                    if(i != index):
                        newEntry.append(item[i])
                sample.append(newEntry)
        sample.remove([])
        return sample

    def buildDecisionTree(self,dataset, attributes, classAttributename, countrecursion,validationset):
        countrecursion += 1
        dataset = dataset[:]
        vals = [record[attributes.index(classAttributename)] for record in dataset]
        default = self.getmostfrequentvalue(attributes, dataset, classAttributename)
        if not dataset or (len(attributes) - 1) <= 0:
            return default
        elif vals.count(vals[0]) == len(vals):
            return vals[0]
        else:
            best = self.getmostLikelyAttribute(dataset, attributes, classAttributename,validationset)
            tree = {best:{}}
            for val in self.getcolumnValues(dataset, attributes, best):
                examples = self.samples(dataset, attributes, best, val)
                newAttr = attributes[:]
                newAttr.remove(best)
                if self.accuracyList and len(self.accuracyList)>1 and GetaccuracyPercentage(givenclassValues,predictedList)>self.accuracyList[-1]:

                    subtree = self.buildDecisionTree(examples, newAttr, classAttributename, countrecursion,validationset)
                    tree[best][val] = subtree
                    self.accuracyList.append(GetaccuracyPercentage(givenclassValues,predictedList))


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
    for i in range(0,10):
        random.shuffle(data)
        x=len(data)
        trainindex=int(0.9*x)
        testindex=int(0.1*x)
        validationindex=int(0.25*x)
        train_data = data[:trainindex]
        test_data = data[-testindex:]
        global validationset
        validationset=train_data[:validationindex]
        tree = treebuilder().buildDecisionTree(train_data, attributes, classAttributename, 0,validationset)
        print "\n------------------------Final Decision tree----------------"
        print str(tree)
        #Testing the data
        print '\nTesting the data.......\n'
        for i in xrange(0,len(test_data)):
            givenclassValues.append(test_data[i][classindex])
        #input dictionary tree

        count = 0
        for entry in test_data:
            count += 1
            dictree = tree.copy()
            result = ""
            while(isinstance(dictree, dict)):
                root = Tree(dictree.keys()[0], dictree[dictree.keys()[0]])
                dictree = dictree[dictree.keys()[0]]
                index = attributes.index(root.value)
                value = entry[index]
                if(value in dictree.keys()):
                    child = Tree(value, dictree[value])
                    result = dictree[value]
                    dictree = dictree[value]
                else:
                    result = list(set(givenclassValues))[randint(0,set(givenclassValues).__len__()-1)]
                    break
            predictedList.append(result)
            #print ("entry%s = %s" % (count, result))
    print len(predictedList)
    print givenclassValues
    for i in range(0,len(predictedList)):
        print('Given Class =' + str(givenclassValues[i]) + ', Predicted Class =' + str(predictedList[i]))
    percentagecorrect = GetaccuracyPercentage(givenclassValues, predictedList)
    print('\nSimple Accuracy:' +' -->'+ str(percentagecorrect) + '%\n')
    print ('Generalized error rate:' +  str(1-((percentagecorrect)/100)))
    #performanceMeasure(givenclassValues,predictedList)
    #precision=TP/(TP+FP)
    #recall=TP/(TP+FN)
    #print precision,recall
    confusionMatrix = [[0 for x in range(set(givenclassValues).__len__())] for x in range(set(givenclassValues).__len__())]
    listOp=list(set(givenclassValues))
    for i in range(0,len(predictedList)):
        given=givenclassValues[i]
        predicted=predictedList[i]
        for j in range(0,len(listOp)):
            for k in range(0,len(listOp)):
                if(given==listOp[j] and predicted==listOp[k]):
                    confusionMatrix[j][k]=confusionMatrix[j][k]+1
    print '\nThe Confusion matrix after classifications is below:\n'
    for i in range(0,set(givenclassValues).__len__()):
        print confusionMatrix[i]
    columndict={}
    rowdict={}
    precision={}
    recall={}
    balancedaccuracy={}
    fscore={}
    falsepositiverate={}
    for i in range(0,set(givenclassValues).__len__()):
        for k in range(0,set(givenclassValues).__len__()):
            if i in rowdict:
                rowdict[i]=rowdict[i]+confusionMatrix[i][k]
            else:
                rowdict[i]=confusionMatrix[i][k]
        columndict[i]=sum(row[i] for row in confusionMatrix)
    print '\n\n'
    for p in range(0,set(givenclassValues).__len__()):
        precision[p] = confusionMatrix[p][p]/float(rowdict[p])
        recall[p]=confusionMatrix[p][p]/float(columndict[p])
        balancedaccuracy[p]=(precision[p]+recall[p])/float(2)
        fscore[p]=2*(precision[p]*recall[p])/float((precision[p]+recall[p]))
        falsepositiverate[p]=(sum(confusionMatrix[p])-confusionMatrix[p][p])/(float(sum(confusionMatrix[p])))
        print '\nThe balanced sample accuracy for class'+ str(p)+ ' is ' + str(balancedaccuracy[p]) + '\n'
        print '\nThe F1 score for class',str(p) + ' is ' + str(fscore[p]) + '\n'
        print '\nThe precision value for class',str(p) + ' is ' + str(precision[p]) + '\n'
        print '\nThe recall value for class',str(p)+' is '+str(recall[p]) + '\n'
        print '\nThe false positive rate value for class',str(p)+' is '+str(falsepositiverate[p]) + '\n'

    plt.plot(recall.values(), precision.values())
    plt.xlabel('Recall values')
    plt.ylabel('Precision values')
    plt.title('--------------------Precision-Recall Curve--------------------')
    plt.show()

    plt.plot(recall.values(), falsepositiverate.values())
    plt.xlabel('Recall values')
    plt.ylabel('False positive Rate values')
    plt.title('--------------------ROC Curve--------------------')
    plt.show()








