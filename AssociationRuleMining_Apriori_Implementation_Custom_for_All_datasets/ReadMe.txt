Program running instructions:
1)	 Run the program quickly to analyse all the outputs form a to f on a small dataset.
   python rules.py adult-stretch.data confidence 0.4 0.55 0.4

2)	The association rules program argument format is like 

python rules.py [filename] [Type of pruning: confidence/lift] [minimum support] [minimum confidence] [minimum lift]

In which every parameter is mandatory and appropriate error handling has been coded to prompt with running instructions.

              Example run on car dataset : 
python rules.py car.data lift 0.4 0.55 0.4


All the outputs are displayed with proper messages and instructions.


3)	The sparse matrix program runs like :
python sparse.py car.data

      Its format is python sparse.py [filename]

Tasks:

Apriori algorithm. Implement the Apriori algorithm by rst determining frequent
itemsets and then proceeding to identify association rules. Consider that the input to your program is a
sparse matrix where the rows are transactions and columns are items. Each value in your matrix is a binary
variable from f0; 1g that indicates presence of an item in the transaction.
a) Implement both Fk􀀀1  F1 and Fk􀀀1  Fk􀀀1 methods. Allow in your code to track the
number of generated candidate itemsets as well as the total number of frequent itemsets.
b) Use three data sets from the UCI Machine learning repository to test your algorithms.
The data sets should contain at least 1000 examples, and at least one data set should contain 10,000
examples or more. You can convert any classication or regression data set into a set of transactions
and you are allowed to discretize all numerical features into two or more categorical features. Compare
these two candidate generation methods on each of the three data sets for three dierent meaningful
levels of the minimum support threshold (the thresholds should allow you to properly compare dierent
methods and make useful conclusions). Provide the numbers of candidate itemsets considered in a table
and discuss the observed savings that one of these methods achieves.
c) Enumerate the number of frequent closed itemsets as well as maximal frequent itemsets
on each of your data sets for each of the minimum support thresholds from the previous question.
Compare those numbers with the numbers of frequent itemsets.
d) Implement condence-based pruning to enumerate all association rules for a given set of
frequent itemsets. Use the previous data sets, with three levels of support and three levels of condence
to quantify the savings in the number of generated condent rules compared to the brute-force method.

e) For each data set and each minimum support threshold, select three condence levels for
which you will generate association rules. Identify top 10 association rules for each combination of
support and condence thresholds and discuss them (i.e. comment on their quality or peculiarity).
Select data sets where you can more easily provide meaningful comments regarding the validity of
rules.
f) Instead of condence, use lift as your measure of rule interestingness. Identify top 10 rules
for each of the previous situations and discuss the relationship between condence and lift.
No specialized libraries are allowed for this task. Make sure that you code runs and submit all the code you
used in this task, including the code that converts data sets from UCI Machine Learning repository into a
transaction data set. Do not include raw data sets in your supplement; however, do provide links to the data
sets you used such that your code can be run independently and its performance can be veried.
Problem 4. (30 points) Formalizing clustering is dicult. In this question you will read two scientic