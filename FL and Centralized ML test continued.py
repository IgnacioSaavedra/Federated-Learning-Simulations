import multiprocessing
import os
import random
import time
import pandas as pd
import numpy as np
import tensorflow as tf
import csv
import shutil
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import f1_score, accuracy_score,recall_score,precision_score
from sklearn.model_selection import train_test_split





def server():#FL Server
    #os.system('cmd /k python server.py')
    os.system('cmd /c python server.py')

def client(n):#FL Client
    time.sleep(10)#Time buffer to start the server
    os.system("cmd /c python Clients/client"+str(n)+".py")
    
    
def centralized_nn(subject_list,results_file):#The centralized model, used for comparison 
    # load the dataset
    dataset = pd.read_csv(data_file, encoding='utf-8')
    #Filter the data from the clientes specified by client_list
    
    # split into input (X) and output (y) variables
    X_total = dataset.iloc[:,0:dataset.shape[1]-7]
    y_total = dataset.iloc[:,dataset.shape[1]-7:dataset.shape[1]]
    
    #Split the test data
    _, x_test,_, y_test = train_test_split(X_total, y_total, test_size=0.3, random_state=1)
    y_test=y_test.iloc[:,1:dataset.shape[1]]#Filter the subject column out of y_test
    
    #Train data is filtered so it comes only from the specified subjects, test data will remain the same
    #Create a list to store the data from the rest of the subjects
    dataframe_list=[]
    for subject in subject_list:
        #Append the data from each subject to the list
        dataframe_list.append(dataset[dataset['subject']==subject])
    #Join all data from the subjects into a single list
    train_data = pd.concat(dataframe_list,axis=0)
    
    
    #The train data has been filtered and now must be randomly selectec
    X = train_data.iloc[:,0:dataset.shape[1]-7]
    y = train_data.iloc[:,dataset.shape[1]-7:dataset.shape[1]]
    x_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=1)
    #Subject is filtered out
    y_train=y_train.iloc[:,1:dataset.shape[1]]
    

    #Define the model
    model=tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(20, activation='relu'))
    model.add(tf.keras.layers.Dense(10, activation='relu'))
    model.add(tf.keras.layers.Dense(6,activation=tf.nn.softmax))
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    #Train the model
    model.fit(x_train,y_train, epochs=100)
    #Test the model
    y_pred = model.predict(x_test)
    y_pred=np.argmax(y_pred, axis=1)
    y_test2=y_test.to_numpy()
    y_test2=np.argmax(y_test2, axis=1)
    val_loss,val_acc = model.evaluate(x_test,y_test)
    #Save metrics to lists: accuracy, loss, centralized and number of clients
    
    resultsDF = pd.read_csv(results_file, encoding='utf-8') 

    
    current_results = {"Accuracy": [val_acc],"Loss":[val_loss],"Number of Clients":[len(client_list)],"Centralized":["Centralized"]}
    current_results = pd.DataFrame(current_results)
    resultsDF=pd.concat([resultsDF,current_results])
    resultsDF.to_csv(results_file, index=False)



if __name__ == "__main__":
    data_file="integrated data/readied data.csv"
    results_file="results.csv"
    results_columns_names=["Accuracy","Loss","Number of Clients","Centralized"]
    subjects = [17,18,19,20]#Number of subjects that remain to be tested for
    number_of_experiments=[2,10,10,10]#Number of times that the experiment remain to be run, corresponds the number of subjects of the previous list
    for i in range(len(subjects)):#A list of the number of clients to use in the multiple tests
        for _ in range(number_of_experiments[i]):
            number_of_clients=subjects[i]
            #The server file is modified to take the number of clientes as a minumum, so all clients and no less are used
            original = 'server.py'
            
            #The reader won't take a .py file, but it will take a .txt file that is almost exactly the same
            target = 'server.txt'
            #Make sure the txt file is an exact copy of the .py file
            shutil.copyfile(original, target)
            target2='server.py'
            
            with open(target, 'r+') as f:
                with open(target2, 'w') as g:
                    lines = f.readlines()
                    for line in lines:
                        #Change the line specifying the number of clients
                        if line.startswith('    number_of_clients='):
                            g.write(line.replace(line,'    number_of_clients='+str(number_of_clients)+"\n"))
            
                        else:
                            g.write(line)
            f.close()
            g.close()
            
            
            #Chose from the 30 clients at random
            client_list=random.sample(range(1, 31), number_of_clients)
            
            #Perform centralized learning and save the results to result file 
            centralized_nn(client_list,results_file)
            
            #break#added for testing purposes
            # Number of processes to create (Clients+ 1 server)
            # Create a list of jobs and then iterate through
            # the number of processes appending each process to
            # the job list 
            jobs = []
            
            
            process_server = multiprocessing.Process(target=server)
            #process_server.start()
            jobs.append(process_server)
            
            for number in client_list:
            #for i in range(0, n_clientes):
            
                process = multiprocessing.Process(target=client, 
                                                  args=[number,])
                jobs.append(process)
        
            # Start the processes (i.e. calculate the random number lists)      
            for j in jobs:
                j.start()
        
            # Ensure all of the processes have finished
            for j in jobs:
                j.join()
            #process_server.join()
            time.sleep(2)
            #break#added for testing purposes