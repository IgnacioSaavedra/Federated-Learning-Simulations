import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier


#Select most relevant features for each possible label
data_path=r'integrated data/'


data=pd.read_csv(data_path+'processed data.csv', encoding='utf-8')

X = data.iloc[:,:561]  #independent columns
features=[]
feature_number=15#Number of most important feature to use per label
for i in range(6):
    y = data.iloc[:,data.shape[1]-i-1]    #target column i.e price range
    model = ExtraTreesClassifier()
    model.fit(X,y)

    feat_importances = pd.Series(model.feature_importances_, index=X.columns)
    feat_importances.nlargest(feature_number).plot(kind='barh')
    
    features=features+feat_importances.nlargest(feature_number).index[0:feature_number].tolist()#Agregar las 15 mejores caracteristicas a la lista
 
    

features = list(dict.fromkeys(features)) #Eliminate duplicates from the features list,as labels might share at least some important labels
#Filtes the data to take only the remaining features
data = pd.concat([data[features], data.iloc[:,data.shape[1]-7:data.shape[1]]], axis=1)

data.to_csv(data_path+'readied data.csv', index=False,header=True)