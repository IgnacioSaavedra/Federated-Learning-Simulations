import pandas as pd
import numpy as np
import os

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)


#file paths
original_train_path=r'raw data/UCI HAR Dataset/train'
original_test_path=r'raw data/UCI HAR Dataset/test'
new_train_path=r'treated data/train'
new_test_path=r'treated data/test'

#If the new folders don't exist, they will be created
if (not os.path. isdir(r'treated data')):
    os. mkdir(r'treated data')
if (not os.path. isdir(new_train_path)):
    os. mkdir(new_train_path)
if (not os.path. isdir(new_test_path)):
    os. mkdir(new_test_path)


#features txt have double spaces randomly, they will be replaced with single spaces
#And then the first column will be erased
#And the files will be converted to csv and saved to a new folder
def delete_string(string, original_file, new_file):
    # Read in the file
    with open(original_file, 'r') as file :
      filedata = file.read()
    
    # Replace the target string
    filedata = filedata.replace('  ', ' ')
    #All remaing spaces can be changed with commas to turn the file into a csv
    filedata = filedata.replace(' ', ',')
    # Write the file out again
    
    with open(new_file, 'w') as file:
      file.write(filedata)
    
    #At the start of each row there used to be a double space, by now it has been replaced with a comma
    #Making it so there is and extra empty column in the csv, the following code will delete it
    csv_file = pd.read_csv(new_file, encoding='utf-8',header=None,delimiter=',')
    csv_file=csv_file.drop([0], axis=1)
    csv_file.to_csv(new_file, index=False,header=False)
   

delete_string("  ",original_train_path+"/"+"X_train.txt",new_train_path+"/"+"X_train.csv")
delete_string("  ",original_test_path+"/"+"X_test.txt",new_test_path+"/"+"X_test.csv")





#Subject train and label files are in chinses for some reason. Ther will be read and then saved in english
def initial_processing_label_subject(original_file, new_file):
    train = pd.read_csv(original_file, encoding='utf-8',header=None,delimiter=' ')
    train.to_csv(new_file, index=False,header=False)

initial_processing_label_subject(original_train_path+"/"+"y_train.txt",new_train_path+"/"+"y_train.csv")
initial_processing_label_subject(original_train_path+"/"+"subject_train.txt",new_train_path+"/"+"subject_train.csv")
initial_processing_label_subject(original_test_path+"/"+"y_test.txt",new_test_path+"/"+"y_test.csv")
initial_processing_label_subject(original_test_path+"/"+"subject_test.txt",new_test_path+"/"+"subject_test.csv")