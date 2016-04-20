import sys
items = []
itemsets = []
print '********  Sparse Matrix Calculation Starts  ************\n'
if len(sys.argv) < 2:
    print 'Too few Arguments'
    print 'Usage: python sparse.py [filename]'
    print 'Sample Usage: python sparse.py adult+stretch.data'
    sys.exit(1)
elif len(sys.argv) > 2:
    print "Too many arguments"
    print 'Usage: python sparse.py [filename]'
    print 'Sample Usage: python sparse.py adult+stretch.data'
else:

    inputfile= str(sys.argv[1])
    if inputfile=='flare.data2':
        x=' '
    else:
        x=','
    infile=open(inputfile,'r')
    for line in infile:
        itemset = line.strip().split(x)
        if itemset:
            itemsets.append(sorted(itemset))
            for item in itemset:
                if item not in items:
                    items.append(item)

    sparsematrix = [[0 for x in range(len(items))] for x in range(len(itemsets))]
    for i in xrange(0,len(itemsets)):
        for j in xrange(0,len(itemsets[i])):
            index=items.index(itemsets[i][j])
            sparsematrix[i][index]=1
    print '    '
    for item in range(0,len(items)):
        print items[item],' ',

    print '\n'
    for value in sparsematrix:
        for item in value:
            print item,'    ',
        print '\n'
    print '\n********  Sparse Matrix Calculation Ends ************'




