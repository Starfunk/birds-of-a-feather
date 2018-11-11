#Finding BOAF weights using a decision tree of depth 2
import pandas as pd
import numpy as np
import operator


df = pd.read_csv("trainingdata.csv")
header = ["nw_1","nw_2","unsolvable"] #for question class
N = 70000 #number of iterations, should be set to 70000 for training.
df = df[df.Trees != 0] #formatting the dataset
df = df.iloc[:,[1,2,4]] #formatting the dataset
rows = df.shape[0]
print("----Starting Analysis----")

class Question:
    """A Question is used to partition a dataset.

    This class just records a 'column number' (e.g., 0 for Color) and a
    'column value' (e.g., Green). The 'match' method is used to compare
    the feature value in an example to the feature value stored in the
    question. See the demo below. This Question class has been modified from
    https://github.com/random-forests/tutorials/blob/master/decision_tree.ipynb
    """
    def __init__(self, column, value):
		
        self.column = column #stores the attribute we are asking about
        self.value = value

    def __repr__(self): #this is just a helper method to print the question
        condition = ">="
        return "Is %s %s %s?" % (
        header[self.column], condition, str(self.value))
      
def entropy(df,rows):
    unsolvables = df.iloc[:,2] #returns df of just unsolvable column
    ones = unsolvables.sum() #summation of all the ones
    zeros = rows - ones #number of zeros in unsolvable column
    if ones == 0:
        entropy1 = 0
    else:
        entropy1 = -(ones/rows) * np.log2(ones/rows)
    if zeros == 0:
        entropy2 = 0
    else:
        entropy2 = -(zeros/rows) * np.log2(zeros/rows)
    entropy = entropy1 + entropy2	
    return entropy
    
def info_gain(prev_ent,ent1,ent2,rows,rows1,rows2):
    return(prev_ent - ( (rows1/rows) * ent1 + (rows2/rows) * ent2))
          
all_questions = {} 
prev_entropy = entropy(df,rows)

for i in range(rows): 
    for k in range(0,2): #k indexes the columns pair-count and zeros
        q = Question(k,df.iat[i,k])
        if k == 0: #NW1 (i.e. 120 - paircount)
            partition_true = df[df.NW1 >= q.value] #df with all values lower than or equal to the question
            rows1 = partition_true.shape[0]
            partition_false = df[df.NW1 < q.value] #df with all values greater than the question
            rows2 = partition_false.shape[0]
        elif k == 1: # NW2 (i.e. number of zeros in A^2)
            partition_true = df[df.NW2 >= q.value] #df with all values lower than or equal to the question
            rows1 = partition_true.shape[0]
            partition_false = df[df.NW2 < q.value] #df with all values greater than the question
            rows2 = partition_false.shape[0]
        entropy_true = entropy(partition_true,rows1) #entropy of the true partition
        entropy_false = entropy(partition_false,rows2) #entropy of the false partition
        information_gain = info_gain(prev_entropy, entropy_true, entropy_false,rows,rows1,rows2)
        if k == 0:
            all_questions[str(i)+'a'] = information_gain
        if k == 1:
            all_questions[str(i)+'b'] = information_gain

max_info_gain = max(all_questions.items(), key=operator.itemgetter(1))[0] # returns column and value of max info-gain

if 'a' in max_info_gain: #an 'a' means the value is in the n1 column
    num_info_gain = int(max_info_gain.replace("a", "")) #turning the dict. key into an integer
    max_column = 0
elif 'b' in max_info_gain: #a 'b' means the value is in the nw2 column
    num_info_gain = int(max_info_gain.replace("b", ""))
    max_column = 1

#Now with highest information gain question established for depth 1 of the tree
#we now find the second best question to ask to get the least-mixed distribution
#in the second layer (depth 2).

best_Q1 = Question(max_column,df.iat[num_info_gain,max_column]) #This is the question to ask for max info-gain.

if best_Q1.column == 0: #formatting df for second layer.
    df = df[df.NW1 >= best_Q1.value] #df with all values lower than or equal to the question.

elif best_Q1.column == 1: 
    df = df[df.NW2 >= best_Q1.value]
        
#partition_true will have a mixture since we have both false-positives and FFUDs 
#while partition_false will not have a mixture because we can choose the distribution
#to not include any 1s (in the unsolvable column). In other words, the algorithm
#selects the question that puts the mixture in partition_true and leaves
#partition_false 100% unmixed.

def entropy2(df,rows):
    unsolvables = df.iloc[:,1] #returns df of just unsolvable column
    ones = unsolvables.sum() #summation of all the ones
    zeros = rows - ones #number of zeros in unsolvable column
    if ones == 0:
        entropy1 = 0
    else:
        entropy1 = -(ones/rows) * np.log2(ones/rows)
    if zeros == 0:
        entropy2 = 0
    else:
        entropy2 = -(zeros/rows) * np.log2(zeros/rows)
    entropy = entropy1 + entropy2	 
    return entropy

if best_Q1.column == 0: #If first question is NW1, then second must be NW2
    df = df.iloc[:,[1,2]]
    rows = df.shape[0]
    all_questions2 = {} 
    prev_entropy = entropy2(df,rows)
    for i in range(rows):
        q = Question(1,df.iat[i,0])
        partition_true = df[df.NW2 >= q.value] #df with all values lower than or equal to the question
        rows1 = partition_true.shape[0]
        partition_false = df[df.NW2 < q.value] #df with all values greater than the question
        rows2 = partition_false.shape[0]
        entropy_true = entropy2(partition_true,rows1) #entropy of the true partition
        entropy_false = entropy2(partition_false,rows2) #entropy of the false partition
        information_gain = info_gain(prev_entropy, entropy_true, entropy_false)
        all_questions2[i] = information_gain
    max_info_gain = max(all_questions2.items(), key=operator.itemgetter(1))[0] #column and value of max info gain
    best_Q2 = Question(1,df.iat[max_info_gain,0])

elif best_Q1.column == 1: #If first question is NW2, then second must be NW1
    df = df.iloc[:,[0,2]]
    rows = df.shape[0]
    all_questions2 = {} 
    prev_entropy = entropy2(df,rows) 
    for i in range(rows):
        print(i)
        q = Question(0,df.iat[i,0])
        partition_true = df[df.NW1 >= q.value] #df with all values lower than or equal to the question
        rows1 = partition_true.shape[0]
        partition_false = df[df.NW1 < q.value] #df with all values greater than the question
        rows2 = partition_false.shape[0]
        entropy_true = entropy2(partition_true,rows1) #entropy of the true partition
        entropy_false = entropy2(partition_false,rows2) #entropy of the false partition
        information_gain = info_gain(prev_entropy, entropy_true, entropy_false,rows,rows1,rows2)
        all_questions2[i] = information_gain 
    max_info_gain = max(all_questions2.items(), key=operator.itemgetter(1))[0] #column and value of max info gain
    best_Q2 = Question(0,df.iat[max_info_gain,0])        

print("The question that best splits the dataset in layer 1 is: ")
print(best_Q1)
print("The question that best splits the dataset in layer 2 is: ")
print(best_Q2)
