import pandas as pd
import numpy as np
import os
#Unify all data from the different files into one


#file paths
train_path=r'treated data/train/'
test_path=r'treated data/test/'
data_path=r'integrated data/'



#If the new folders don't exist, they will be created
if (not os.path. isdir(r'integrated data')):
    os. mkdir(r'integrated data')




# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

X_train = pd.read_csv(train_path+'X_train.csv', encoding='utf-8',header=None)
X_test = pd.read_csv(test_path+'X_test.csv', encoding='utf-8',header=None)
y_train = pd.read_csv(train_path+'y_train.csv', encoding='utf-8',header=None)
y_test = pd.read_csv(test_path+'y_test.csv', encoding='utf-8',header=None)
subject_test = pd.read_csv(test_path+'subject_test.csv', encoding='utf-8',header=None)
subject_train = pd.read_csv(train_path+'subject_train.csv', encoding='utf-8',header=None)


#Append all columns from train and test files
train=pd.concat([X_train,subject_train,y_train],axis=1)
test=pd.concat([X_test,subject_test,y_test],axis=1)
#Append all rows from train and test files into a single dataframe
data=train.append(test)


#save the dataframe
data.to_csv(data_path+'data.csv', index=False,header=False)