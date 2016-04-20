import matplotlib.pyplot as bplot
from pylab import plot, show, savefig, xlim, figure, hold, ylim, legend, boxplot, setp, axes
import numpy as np
def read_data(fname):
    sepalLength = []
    sepalWidth=[]
    petalLength=[]
    petalWidth=[]
    classflower=[]
    file = open(fname, 'r');
    for line in file:
        dataline = [w.lower() for w in line.split(',')]
        sepalLength.append(float(dataline[0].strip()))
        sepalWidth.append(float(dataline[1].strip()))
        petalLength.append(float(dataline[2].strip()))
        petalWidth.append(float(dataline[3].strip()))
        classflower.append(dataline[4])
    return sepalLength,sepalWidth,petalLength,petalWidth,classflower

def setBoxColors(bp):
    setp(bp['boxes'][0], color='blue')
    setp(bp['caps'][0], color='blue')
    setp(bp['caps'][1], color='blue')
    setp(bp['whiskers'][0], color='blue')
    setp(bp['whiskers'][1], color='blue')
    setp(bp['fliers'][0], color='blue')
    setp(bp['fliers'][1], color='blue')
    setp(bp['medians'][0], color='blue')

    setp(bp['boxes'][1], color='red')
    setp(bp['caps'][2], color='red')
    setp(bp['caps'][3], color='red')
    setp(bp['whiskers'][2], color='red')
    setp(bp['whiskers'][3], color='red')
    setp(bp['fliers'][2], color='red')
    setp(bp['fliers'][3], color='red')
    setp(bp['medians'][1], color='red')

if __name__== "__main__":
    trainfile='iris.data'
    sepalLength,sepalWidth,petalLength,petalWidth,classflower = read_data(trainfile)
    print "*********************** PART A *****************"
    print "Standard Deviation of sepal length values is: ",np.std(sepalLength)
    print  "Mean of sepal length values is: ",np.mean(sepalLength),"\n"
    print "Standard Deviation of sepal Width values is: ",np.std(sepalWidth)
    print  "Mean of sepal Width values is: ",np.mean(sepalWidth),"\n"
    print "Standard Deviation of petal length values is: ",np.std(petalLength)
    print  "Mean of petal length values is: ",np.mean(petalLength),"\n"
    print "Standard Deviation of petal width values is: ",np.std(petalWidth)
    print  "Mean of petal width values is: ",np.mean(petalWidth)
    print "*********************** PART A ENDS *****************"

    print "*********************** PART B *****************"
    print "*********************** Calculation for Iris-setosa *****************"
    print "Standard Deviation of sepal length values for Iris-setosa is: ",np.std(sepalLength[:50])
    print  "Mean of sepal length values for Iris-setosa is : ",np.mean(sepalLength[:50])
    print "Standard Deviation of sepal Width values for Iris-setosa is: ",np.std(sepalWidth[:50])
    print  "Mean of sepal Width valuesfor  Iris-setosa is: ",np.mean(sepalWidth[:50])
    print "Standard Deviation of petal length values Iris-setosa is: ",np.std(petalLength[:50])
    print  "Mean of petal length values for Iris-setosa is: ",np.mean(petalLength[:50])
    print "Standard Deviation of petal width values for Iris-setosa is: ",np.std(petalWidth[:50])
    print  "Mean of petal width values for Iris-setosa is: ",np.mean(petalWidth[:50]),"\n"
    print "*********************** Calculation for Iris-versicolor *****************"
    print "Standard Deviation of sepal length values for Iris-versicolor is: ",np.std(sepalLength[50:101])
    print  "Mean of sepal length values for Iris-versicolor is: ",np.mean(sepalLength[50:101])
    print "Standard Deviation of sepal Width values for Iris-versicolor is: ",np.std(sepalWidth[50:101])
    print  "Mean of sepal Width values for Iris-versicolor is: ",np.mean(sepalWidth[50:101])
    print "Standard Deviation of petal length values for Iris-versicolor is: ",np.std(petalLength[50:101])
    print  "Mean of petal length values for Iris-versicolor is: ",np.mean(petalLength[50:101])
    print "Standard Deviation of petal width values for Iris-versicolor is: ",np.std(petalWidth[50:101])
    print  "Mean of petal width values for Iris-versicolor is: ",np.mean(petalWidth[50:101]),"\n"

    print "*********************** Calculation for Iris-virginica *****************"

    print "Standard Deviation of sepal length values for Iris-virginica is: ",np.std(sepalLength[100:151])
    print  "Mean of sepal length values for Iris-virginica is: ",np.mean(sepalLength[100:151])
    print "Standard Deviation of sepal Width values for Iris-virginica is: ",np.std(sepalWidth[100:151])
    print  "Mean of sepal Width values for Iris-virginica is: ",np.mean(sepalWidth[100:151])
    print "Standard Deviation of petal length values for Iris-virginica is: ",np.std(petalLength[100:151])
    print  "Mean of petal length values for Iris-virginica is: ",np.mean(petalLength[100:151])
    print "Standard Deviation of petal width values for Iris-virginica is: ",np.std(petalWidth[100:151])
    print  "Mean of petal width values for Iris-virginica is: ",np.mean(petalWidth[100:151])

    print "*********************** PART B ENDS *****************"

    print "*********************** PART C Starts *****************"

    bplot.boxplot([sepalLength[:50],sepalLength[50:101],sepalLength[100:151]])
    bplot.xticks([1,2,3],['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
    bplot.ylabel('<---------------------Sepal Length in centimetres------------------------>')
    bplot.xlabel('<------------------------Flower names------------------------------------>')
    bplot.title('Blox plot of Sepal length for three different flowers')
    savefig('boxplotSepalLength.png')
    show()

    bplot.boxplot([sepalWidth[:50],sepalWidth[50:101],sepalWidth[100:151]])
    bplot.xticks([1,2,3],['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
    bplot.ylabel('<---------------------Sepal Width in centimetres------------------------>')
    bplot.xlabel('<------------------------Flower names------------------------------------>')
    bplot.title('Blox plot of Sepal Width for three different flowers')
    savefig('boxplotSepalWidth.png')
    show()


    bplot.boxplot([petalLength[:50],petalLength[50:101],petalLength[100:151]])
    bplot.xticks([1,2,3],['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
    bplot.ylabel('<---------------------Petal Length in centimetres------------------------>')
    bplot.xlabel('<------------------------Flower names------------------------------------>')
    bplot.title('Blox plot of Petal length for three different flowers')
    savefig('boxplotPetalLength.png')
    show()

    bplot.boxplot([petalWidth[:50],petalWidth[50:101],petalWidth[100:151]])
    bplot.xticks([1,2,3],['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
    bplot.ylabel('<---------------------Petal Width in centimetres------------------------>')
    bplot.xlabel('<------------------------Flower names------------------------------------>')
    bplot.title('Blox plot of Petal Width for three different flowers')
    savefig('boxplotpetalWidth.png')
    show()

    print "*********************** PART C Ends *****************"