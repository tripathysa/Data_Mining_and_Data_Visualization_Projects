Program running instructions:
1)	Run the program by running “python Recommender.py”.Please make sure that the input files are in same directory as the program file.
2)	Inputs are hardcoded in the program in the main function() from Line number 310
3)	Currently the inputs are given as 

    datafile='u1.base'
    moviefile='u.item'
    userfile='u.user'
    occupationfile='u.occupation'
    testfile= 'u1.test'
    recommender = Recommender()
    distancemetric='euclidean'  #euclidean,manhattan,lmax
#   recommender.naive(testfile,datafile)
    algo='parta' # parta or partb

 You can change the training file by changing datafile, testfile by changing testfile, distance by distancemetric, and part a or part b of question by changing algo value as parta or partb respectively

4)	For running the naïve strategy, Uncomment the code in line no 319, and comment line numbers 321 and 322.

5)CurseofDimensionality.py requires matplotlib library of python to plot the graph.
