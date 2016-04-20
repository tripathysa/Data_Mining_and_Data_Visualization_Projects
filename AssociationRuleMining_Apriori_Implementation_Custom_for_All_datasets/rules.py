import sys
import copy

class associationRules:

    def printandwriteAssociationRules(self,rules,numberofrules,pruningtype):

        outfile= open('output.txt','w')
        for entity in sorted(rules.keys(), reverse=True):
            if pruningtype=='lift' and numberofrules>10:
                break
            if len(rules[entity]) > 1:
                for rule in rules[entity]:
                    print "%s => %s (%s)\n" % (rule[0],
                        rule[1], entity)
                    outfile.write("%s => %s (%s)\n" % (rule[0],
                        rule[1], entity))
                    numberofrules += 1
            else:
                print "%s => %s (%s)\n" % (rules[entity][0][0],
                    rules[entity][0][1], entity)
                outfile.write("%s => %s (%s)\n" % (rules[entity][0][0],
                    rules[entity][0][1], entity))
                numberofrules += 1


        return numberofrules

    def constructandWriteOutput(self,freqItemsets,typeofset):
        resultdictionary={}
        for i in range(1, len(freqItemsets) + 1):
            if freqItemsets[i]:
                for entity in freqItemsets[i]:
                    if not resultdictionary.has_key(entity[1]):
                        resultdictionary[entity[1]] = [entity[0]]
                    else:
                        resultdictionary[entity[1]].append(entity[0])

        print "******************   writing output  ******************\n"
        num = 0
        if typeofset=='maximal':
            print "\nMaximal sets are:------------->\n"
        elif typeofset=='closed':
            print "\nClosed sets are:------------->\n"

        for entity in sorted(resultdictionary.keys(), reverse=True):
            if entity:
                if len(resultdictionary[entity]) > 1:
                    for itemset in resultdictionary[entity]:
                        print "\n    %s, %s\n" % (itemset, entity)
                        num += 1
                else:
                    print "\n %s, %s\n" % (resultdictionary[entity][0], entity)
                    num += 1
        if typeofset=='maximal':
            print "\n%s Number of maximal sets generated" % num
        elif typeofset=='closed':
            print "\n%s Number of Closed sets generated" % num

    def CalculateSupportCount(self,itemset, itemsets):
        support_count = 0
        for entity in itemsets:
            if isinstance(itemset, list):
                for each_item in itemset:
                    if each_item not in entity:
                        break
                else:
                    support_count += 1
            else:
                if itemset in entity:
                    support_count += 1

        return support_count


    def CalculateSizeOneItemsets(self,distinctitems,transactions,minsupport):
        candidatesetsOne=[]
        freqItemsetsOne=[]
        for entity in distinctitems:
            supportcount = self.CalculateSupportCount(entity, transactions) / float(len(transactions))
            candidatesetsOne.append([[entity], supportcount])
            if supportcount >= minsupport:
                freqItemsetsOne.append([[entity], supportcount])
        return freqItemsetsOne,candidatesetsOne



    def generatecandidatebyFkminusOneFkminusone(self,itemsets):
        candidates = []
        num = len(itemsets)
        if len(itemsets[0]) == 1:
            for n in range(num - 1):
                for m in range(n + 1, num):
                        candidates.append([itemsets[n][0], itemsets[m][0]])
        else:
            for n in range(num - 1):
                for m in range(n + 1, num):
                    if (itemsets[n][:-1] == itemsets[m][:-1]
                        and itemsets[n][1:] + [itemsets[m][-1]] in itemsets):
                        candidates.append(itemsets[n] + [itemsets[m][-1]])

        return candidates

    def gen_candidatebyBruteForce(self,itemsets):
        candidates = []
        num = len(itemsets)
        if len(itemsets[0]) == 1:
            for n in range(num - 1):
                for m in range(n + 1, num):
                        candidates.append([itemsets[n][0], itemsets[m][0]])
        else:
            for n in range(num - 1):
                for m in range(n + 1, num):
                    if (itemsets[n][:-1] == itemsets[m][:-1]
                        and itemsets[n][1:] + [itemsets[m][-1]] in itemsets):
                        candidates.append(itemsets[n] + [itemsets[m][-1]])

        return candidates

    def gen_candidatebyF1(self,itemsets,itemsetOne):
        candidates = []
        num = len(itemsets)
        lenitemOne=len(itemsetOne)
        if len(itemsets[0]) == 1:
            for n in range(num - 1):
                for m in range(n + 1, num):
                        candidates.append([itemsets[n][0], itemsets[m][0]])
        else:
            for n in range(0,num):
                for m in range(0, lenitemOne):
                    if itemsetOne[m][0] not in itemsets[n]:
                        x=sorted(itemsets[n] + [itemsetOne[m][0]])
                        if x not in candidates:
                            candidates.append(x)

        return candidates

    def CheckifSubset(self,itemset1, itemset2):
        for item in itemset1:
            if item not in itemset2:
                return False
            else:
                return True

    def returnMaximalFrequentsets(self,frequent_itemsets):
        size = len(frequent_itemsets)
        for i in range(size, 0, -1):
            if frequent_itemsets[1]:
                for entity in frequent_itemsets[i]:
                    for j in range(i - 1, 0, -1):
                        iter_itemsets = copy.deepcopy(frequent_itemsets[j])
                        for itemset in iter_itemsets:
                            if self.CheckifSubset(itemset[0], entity[0]):
                                frequent_itemsets[j].remove(itemset)
        return frequent_itemsets

    def returnClosedFrequentsets(self,frequent_itemsets):
        closeditemsets = {}
        size = len(frequent_itemsets)
        closeditemsets[size] = frequent_itemsets[size]

        for i in range(1, size):
            closeditemsets[i] = []
            for entity in frequent_itemsets[i]:
                for itemset in frequent_itemsets[i + 1]:
                    if self.CheckifSubset(itemset[0], entity[0]) and itemset[1] == entity[1]:
                        break
                else:
                    closeditemsets[i].append(entity)

        return closeditemsets

    def subtract(self,set1, set2):
        result = []
        for entity in set2:
            if not entity[0] in set1:
                result.append(entity[0])
        return result

    def generateAssociationRulesbyConfidencePruning(self,minimumconfidence, freqitemsets):
        result = {}

        for n in range(2, len(freqitemsets) + 1):
            for itemset in freqitemsets[n]:
                hold = []
                for entity in itemset[0]:
                    hold.append([entity])

                k_itemset = copy.deepcopy(hold)
                count = len(k_itemset)
                for i in range(count - 1):
                    for entity in k_itemset:
                        div = self.subtract(entity, k_itemset)
                        for l in freqitemsets[len(div)]:
                            if sorted(div) == sorted(l[0]):
                                supportcount = l[1]
                                break
                        conf = itemset[1] / supportcount
                        if conf < minimumconfidence:
                            if entity in hold:
                                hold.remove(entity)
                        elif (result.has_key(conf)
                            and [div, entity] not in result[conf]):
                            result[conf].append([div, entity])
                        else:
                            result[conf] = [[div, entity]]

                    if hold:
                        hold = self.generatecandidatebyFkminusOneFkminusone(hold)
                    else:
                        break

        return result
    def generateAssociationRulesbyLiftPruning(self,minimumLift, freqitemsets):
        result = {}

        for n in range(2, len(freqitemsets) + 1):
            for itemset in freqitemsets[n]:
                hold = []
                for entity in itemset[0]:
                    hold.append([entity])

                k_itemset = copy.deepcopy(hold)
                count = len(k_itemset)
                for i in range(count - 1):
                    for entity in k_itemset:
                        div = self.subtract(entity, k_itemset)
                        for l in freqitemsets[len(div)]:
                            if sorted(div) == sorted(l[0]):
                                supportcount = l[1]
                                break
                #calculate lift:
                        for q in freqitemsets[len(entity)]:
                            if sorted(entity) == sorted(q[0]):
                                supportcount1 = q[1]
                                break

                        conf = itemset[1] / supportcount
                        lift=conf/supportcount1
                        if lift < minimumLift:
                            if entity in hold:
                                hold.remove(entity)
                        elif (result.has_key(lift)
                            and [div, entity] not in result[lift]):
                            result[lift].append([div, entity])
                        else:
                            result[lift] = [[div, entity]]

                    if hold:
                        hold = self.generatecandidatebyFkminusOneFkminusone(hold)
                    else:
                        break

        return result


def main():
    rulesobj= associationRules()
    if len(sys.argv) < 6:
        print 'ERROR: Too few Arguments'
        print 'USAGE: python rules.py [filename] [Type of pruning: confidence/lift] [minimum support] [minimum confidence] [minimum lift]'
        print 'SAMPLE USAGE: python rules.py adult+stretch.data confidence 0.4 0.2 1'
        sys.exit(1)
    elif len(sys.argv) > 6:
        print "ERROR: Too many arguments"
        print 'USAGE: python rules.py [filename] [Type of pruning: confidence/lift] [minimum support] [minimum confidence] [minimum lift]'
        print 'SAMPLE USAGE: python rules.py adult+stretch.data confidence 0.4 0.2 1'
    else:
        inputfile= str(sys.argv[1])
        pruningtype= str(sys.argv[2])
        minsupport = float(sys.argv[3])
        minimumconfidence = float(sys.argv[4])
        minimumlift=float(sys.argv[5])
        distinctitems = []
        transactions = []
        freqItemsets = {}
        candidate_sets={}
        if inputfile=='flare.data2':
            x=' '
        else:
            x=','
        #Read the dataset
        infile=open(inputfile,'r')
        #infile=[['Bread','Milk'],['Bread','Diaper','Beer','Egg'],['Milk','Diaper','Beer','Cola'],['Bread','Milk','Diaper','Beer'],['Bread','Milk','Diaper','Cola']]
        for row in infile:
            itemset = row.strip().split(x)
            if itemset:
                for item in itemset:
                    if item not in distinctitems:
                        distinctitems.append(item)
                transactions.append(sorted(itemset))
        print '********  Sparse Matrix Calculation Starts   ************'
        sparsematrix = [[0 for x in range(len(distinctitems))] for x in range(len(transactions))]
        for i in xrange(0,len(transactions)):
            for j in xrange(0,len(transactions[i])):
                index=distinctitems.index(transactions[i][j])
                sparsematrix[i][index]=1
        print '    '
        for item in range(0,len(distinctitems)):
            print distinctitems[item],' ',

        print '\n'
        for value in sparsematrix:
            for item in value:
                print item,'    ',
            print '\n'
        print '********  Sparse Matrix Calculation Ends  ************'


        print '\nDistinct Items in the dataset: --------->',distinctitems
        distinctitems.sort()
        print "\n******************   There are a total of %s item(s) and  %s transaction(s)  ******************\n" % (len(distinctitems), len(transactions))
        print "******************  Working on generation of frequent itemsets   ******************\n"

        # generate the 1-size itemsets
        freqItemsets[1] = []
        candidate_sets[1]=[]
        freqItemsets[1],candidate_sets[1] = rulesobj.CalculateSizeOneItemsets(distinctitems,transactions,minsupport)


        # generate frequent itemset
        frequentOneitems=[]
        for each in freqItemsets[1]:
            frequentOneitems.append(each[0])
        noofiterations = 1
        numberofFkMinusOneFkMinusOneCandidates=0
        numberofFkMinusOneFoneCandidates=0
        #numberofBruteforceCandidates=0
        while noofiterations:
            freqItemsets[noofiterations + 1] = []
            candidate_sets[noofiterations+1]=[]
            k_freq_itemsets = []
            #bruteforceItemsets=[]
            for each in freqItemsets[noofiterations]:
                k_freq_itemsets.append(each[0])
            # for each in candidate_sets[noofiterations]:
            #     bruteforceItemsets.append(each[0])
            #generate candidate itemsets by Brute force
            #bruteforcecandidates=rulesobj.gen_candidatebyBruteForce(bruteforceItemsets)
            #generate candidate itemsets by F(k-1)*F1
            f1candidates=rulesobj.gen_candidatebyF1(k_freq_itemsets,frequentOneitems)
            #generate candidate itemsets by F(k-1)*F(k-1)
            candidates = rulesobj.generatecandidatebyFkminusOneFkminusone(k_freq_itemsets)

            # if bruteforcecandidates:
            #     print '\n\nCandidates by Brute Force:', bruteforcecandidates
            #     numberofBruteforceCandidates=numberofBruteforceCandidates+len(bruteforcecandidates)
            if f1candidates:
                print '\n\nCandidates by F(k-1)* F(1):', f1candidates
                numberofFkMinusOneFoneCandidates=numberofFkMinusOneFoneCandidates+len(f1candidates)
            if candidates:
                print '\n\nCandidates by F(k-1)* F(k-1):', candidates
                numberofFkMinusOneFkMinusOneCandidates=numberofFkMinusOneFkMinusOneCandidates+len(candidates)
            for entity in candidates:
                support = rulesobj.CalculateSupportCount(entity, transactions) / float(len(transactions))
                if support >= minsupport:
                    freqItemsets[noofiterations + 1].append([entity, support])
            # for entity in bruteforcecandidates:
            #     support1 = rulesobj.CalculateSupportCount(entity, transactions) / float(len(transactions))
            #     candidate_sets[noofiterations + 1].append([entity, support1])

            if freqItemsets[noofiterations + 1] == []:
                freqItemsets.pop(noofiterations + 1)
                break

            noofiterations =noofiterations+ 1


        # maximal, closed or rule generation

        print '\nprint frequent itemsets', freqItemsets
        countfreqItems = sum(len(v) for v in freqItemsets.itervalues())
        print '\nTotal number of frequent itemsets generated:', countfreqItems

        #print '\nNumber of candidate sets generated by Brute Force : ', numberofBruteforceCandidates
        print '\nNumber of candidate sets generated by F(k-1)*F(1) :', numberofFkMinusOneFoneCandidates
        print '\nNumber of candidate sets generated by F(k-1)*F(k-1) :', numberofFkMinusOneFkMinusOneCandidates
        if pruningtype=='confidence':

            print "\n******************  Working on generating rules by confidence pruning   ******************"
            rules = rulesobj.generateAssociationRulesbyConfidencePruning(minimumconfidence, freqItemsets)

            print ("\n******************  confidence pruned rules generatation completed  ******************")

            print "\n******************  Writing output for confidence based rules started   ******************\n"
            numberofrules = 0

            print "\n Following confidence based pruned rules are generated: "
            numberofrules=rulesobj.printandwriteAssociationRules(rules,numberofrules,pruningtype)


            print "%s confidence based pruned association rules generated" % numberofrules

        elif pruningtype=='lift':

            print "\n******************  Working on generating rules by Lift pruning   ******************"
            rules1 = rulesobj.generateAssociationRulesbyLiftPruning(minimumlift, freqItemsets)

            print ("\n******************  Lift pruned rules generatation completed  ******************")

            print "\n******************  Writing output for lift based rules started   ******************\n"
            numberofrules = 0

            print "\n Following Lift based pruned rules are generated: "
            numberofrules=rulesobj.printandwriteAssociationRules(rules1,numberofrules,pruningtype)


            print "%s Lift based pruned association rules generated" % numberofrules
        # write the result
        print "\n\n******************  Generating Association rules completed   ******************\n"

        count=0
        for i in range(2,len(freqItemsets.keys())+1):
            count =count + ((2**len(freqItemsets[i]))-2)
        print '\nNumber of rules generated by Brute Force : ', count
        freqClosedItemsets = rulesobj.returnClosedFrequentsets(freqItemsets)
        freqMaximalItemsets = rulesobj.returnMaximalFrequentsets(freqItemsets)
        print "\n******************  Generating Closed Itemsets  ******************\n"
        rulesobj.constructandWriteOutput(freqClosedItemsets,'closed')
        print "\n******************  Generating maximal Itemsets  ******************\n"
        rulesobj.constructandWriteOutput(freqMaximalItemsets,'maximal')

if __name__ == '__main__':
    print 'Starting Association Rule Mining..........................................................................'
    main()