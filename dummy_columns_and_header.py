import pandas as pd
import numpy as np
#replace the Activity column with multiple dummy columns. Important for ML
#Also add a header


data_path=r'integrated data/'



# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

feature_names=pd.read_csv(r'raw data/UCI HAR Dataset/features.txt', encoding='utf-8',header=None,delimiter=' ').loc[:,1]
#Create header with the feature names and "subject" and "activity"
header=pd.concat([feature_names, pd.DataFrame(["subject","activity"])], axis=0)
header=header.loc[:,0].tolist()



#There are repeated names in the header. This will be corrected by adding a suffic
from collections import Counter # Counter counts the number of occurrences of each item
from itertools import tee, count

def uniquify(seq, suffs = count(1)):
    """Make all the items unique by adding a suffix (1, 2, etc).

    `seq` is mutable sequence of strings.
    `suffs` is an optional alternative suffix iterable.
    """
    not_unique = [k for k,v in Counter(seq).items() if v>1] # so we have: ['name', 'zip']
    # suffix generator dict - e.g., {'name': <my_gen>, 'zip': <my_gen>}
    suff_gens = dict(zip(not_unique, tee(suffs, len(not_unique))))  
    for idx,s in enumerate(seq):
        try:
            suffix = str(next(suff_gens[s]))
        except KeyError:
            # s was unique
            continue
        else:
            print(seq[idx])
            seq[idx] += suffix

uniquify(header)

#Load data and add header
data=pd.read_csv(data_path+'data.csv', encoding='utf-8',names=header)

#Activity is a number, before creating the dummy columns the number will be replaced with a descriptor
data=data.replace({'activity' : {1:'WALKING',2:'WALKING_UPSTAIRS',3:'WALKING_DOWNSTAIRS',4:'SITTING',5:'STANDING',6:'LAYING'}})




#Create dummy columns and save
nominal_columns = ["activity"]
dummy_df = pd.get_dummies(data[nominal_columns])
data = pd.concat([data, dummy_df], axis=1)
data = data.drop(nominal_columns, axis=1)

data.to_csv(data_path+'processed data.csv', index=False,header=True)