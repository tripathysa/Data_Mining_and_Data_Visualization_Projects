Program Name:  wine.py          
RUN: python wine.py
Description: Contains all the three parts of the question in the program. 
The program is by default set to run with given un-normalized values.
a)	To run the program with 0-1 normalization: 
               Change read_data() function name to  read_data01normal() at line number 145.

b)	To run the program with z-score normalization: 
             Change read_data() function name to  read_datazscore() at line number 145.


Tasks: 
Download data set Wine and answer the following questions:
a)  Provide pairwise scatter plots for four most correlated and four least correlated pairs of
features, using Pearson's correlation coecient. Label all axes in all your plots and select fonts of
appropriate style and size. Experiment with dierent ways to plot these scatter plots and choose the
one most visually appealing and most professionally looking.
b) Use Euclidean distance to nd the closest example to every example available in the data
set (exclude the class variable). Calculate the percentage of points whose closest neighbors have the
same class label (for data set as a whole and also for each class).
c) Repeat the previous step but after the data set is normalized using rst 0-1 normalization
and then z-score normalization. Investigate the reasons for discrepancy and provide evidence to support
every one of your claims. Provide the code you used for normalizing and visualizing the data.