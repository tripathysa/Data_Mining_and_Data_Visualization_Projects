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
    def __init__(self):
        self.listopattributes=[]
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

    #Calculates the entropy of the given data set for the target attr
    def calculateentropy(self,attributes, dataset, classAttributename):

        Frequency = {}
        EntropyVal = 0.0

        #find index of the target attribute
        i = 0
        for item in attributes:
            if (classAttributename == item):
                break
            ++i

        # Calculate the frequency of each of the values in the target attr
        for item in dataset:
            if (Frequency.has_key(item[i])):
                Frequency[item[i]] += 1.0
            else:
                Frequency[item[i]]  = 1.0

        # Calculate the entropy of the data for the target attr
        for freqitem in Frequency.values():
            EntropyVal += (-freqitem/len(dataset)) * math.log(freqitem/len(dataset), 2)
        return EntropyVal

    def gini(self,attributes, dataset, classAttributename):

        Frequency = {}
        ginival = 0.0

        #find index of the target attribute
        i = 0
        for item in attributes:
            if (classAttributename == item):
                break
            ++i

        # Calculate the frequency of each of the values in the target attr
        for item in dataset:
            if (Frequency.has_key(item[i])):
                Frequency[item[i]] += 1.0
            else:
                Frequency[item[i]]  = 1.0

        # Calculate the entropy of the data for the target attr
        for freq in Frequency.values():
            ginival += ((freq/len(dataset)) ** 2)
        return 1-ginival





    def calculateInformationGain(self,attributes, dataset, attr, classAttributename):
        """
        Calculates the information gain (reduction in entropy) that would
        result by splitting the data on the chosen attribute (attr).
        """
        Frequency = {}
        subsetEntropy = 0.0

        #find index of the attribute
        i = attributes.index(attr)

        # Calculate the frequency of each of the values in the target attribute
        for item in dataset:
            if (Frequency.has_key(item[i])):
                Frequency[item[i]] += 1.0
            else:
                Frequency[item[i]]  = 1.0
        # Calculate the sum of the entropy for each subset of records weighted
        # by their probability of occuring in the training set.
        for val in Frequency.keys():
            valProb        = Frequency[val] / sum(Frequency.values())
            dataSubset     = [item for item in dataset if item[i] == val]
            subsetEntropy += valProb * self.gini(attributes, dataSubset, classAttributename)

        # Subtract the entropy of the chosen attribute from the entropy of the
        # whole data set with respect to the target attribute (and return it)
        return (self.gini(attributes, dataset, classAttributename) - subsetEntropy)

    #choose best attibute
    def chooseAttr(self,dataset, attributes, classAttributename):
        best = attributes[0]
        maxGain = 0;
        for attr in attributes:
            newGain = self.calculateInformationGain(attributes, dataset, attr, classAttributename)
            if newGain>maxGain:
                maxGain = newGain
                best = attr
                self.listopattributes.append(attr)
        return best

    #get values in the column of the given attribute
    def getValues(self,dataset, attributes, attr):
        index = attributes.index(attr)
        values = []
        for item in dataset:
            if item[index] not in values:
                values.append(item[index])
        return values

    def getExamples(self,dataset, attributes, best, val):
        examples = [[]]
        index = attributes.index(best)
        for item in dataset:
            #find entries with the give value
            if (item[index] == val):
                newEntry = []
                #add value if it is not in best column
                for i in range(0,len(item)):
                    if(i != index):
                        newEntry.append(item[i])
                examples.append(newEntry)
        examples.remove([])
        return examples

    def buildDecisionTree(self,dataset, attributes, classAttributename, recursion,m):
        recursion += 1
        print 'top attributes',self.listopattributes
        #Returns a new decision tree based on the examples given.
        dataset = dataset[:]
        vals = [record[attributes.index(classAttributename)] for record in dataset]
        default = self.getmostfrequentvalue(attributes, dataset, classAttributename)

        # If the dataset is empty or the attributes list is empty, return the
        # default value. When checking the attributes list for emptiness, we
        # need to subtract 1 to account for the target attribute.
        if not dataset or (len(attributes) - 1) <= 0:
            return default
        # If all the records in the dataset have the same classification,
        # return that classification.
        elif vals.count(vals[0]) == len(vals):
            return vals[0]
        else:
            # Choose the next best attribute to best classify our data
            best = self.chooseAttr(dataset, attributes, classAttributename)
            best=self.listopattributes[-m:][-1]
            # Create a new decision tree/node with the best attribute and an empty
            # dictionary object--we'll fill that up next.
            tree = {best:{}}

            # Create a new decision tree/sub-node for each of the values in the
            # best attribute field
            for val in self.getValues(dataset, attributes, best):
                # Create a subtree for the current value under the "best" field
                examples = self.getExamples(dataset, attributes, best, val)
                newAttr = attributes[:]
                newAttr.remove(best)
                subtree = self.buildDecisionTree(examples, newAttr, classAttributename, recursion,m)

                # Add the new subtree to the empty dictionary object in our new
                # tree/node we just created.
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
    m=3
    x=len(data)
    trainindex=int(0.9*x)
    testindex=int(0.1*x)
    train_data = data[:trainindex]
    test_data = data[-testindex:]
    tree = treebuilder().buildDecisionTree(train_data, attributes, classAttributename, 0,m)
    print "\n------------------------Final Decision tree----------------"
    print str(tree)
    #Testing the data
    print '\nTesting the data.......\n'
    for i in xrange(0,len(test_data)):
        givenclassValues.append(test_data[i][classindex])
    #input dictionary tree

    count = 0
    for item in test_data:
        count += 1
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
        #print ("item%s = %s" % (count, result))
        print('Given Class =' + str(givenclassValues[count-1]) + ', Predicted Class =' + str(result))
    percentagecorrect = GetaccuracyPercentage(givenclassValues, predictedList)
    print('\nPercentage of class values predicted correctly combining the beam search and decision tree classifier' +' -->'+ str(percentagecorrect) + '%\n')