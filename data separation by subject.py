import pandas as pd
import numpy as np
import os
data_file="integrated data/readied data.csv"
data=pd.read_csv(data_file, encoding='utf-8')
for i in range(30):
    datos_guardar=data[data['subject']==i+1]
    datos_guardar.to_csv('integrated data/readied data subject '+str(i+1)+'.csv', index=False,header=True)