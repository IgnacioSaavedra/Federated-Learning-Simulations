import flwr as fl
import os
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
    
class Client(fl.client.NumPyClient):    
    def get_parameters(self):
        return model.get_weights()
    
    def fit(self, parameters, config):
        model.set_weights(parameters)
        #model.fit(x_train, y_train, epochs=1, batch_size=32, steps_per_epoch=3)
        model.fit(x_train,y_train, epochs=100)
        return model.get_weights(), len(x_train), {}
    
    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(x_test, y_test)
        return loss, len(x_test), {"accuracy": accuracy}
 

           
    
if __name__ == "__main__":
    # Make TensorFlow log less verbose
    print("Staring Client")
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    #This will be saved in a Folder named "Clients" it must go up one folder first
    #Loading the data,there is no subject 0
    subject_number=0
    
    
    #Clients are stored in the Clients folder, so it is necesary to go up one folder first to store the data. Only applies when the script is being run directly, Otherwise it's folder if the script that runs the console that counts
    #folder_list=os.getcwd().split("\\")
    #print(folder_list)
    #folder_up = "/".join(folder_list[0:len(folder_list)-1])
    #print(folder_up)
    #data_file=folder_up+"/integrated data/readied data.csv"
    
    #Note: when this is being run from a console opened by another script, path are relative to the position of the script that opens the console
    data_file="integrated data/readied data subject 0.csv"
    dataset = pd.read_csv(data_file, encoding='utf-8')
    #filter data based on the subject number, to each client corresponds one subject

    X = dataset.iloc[:,0:dataset.shape[1]-7]
    y = dataset.iloc[:,dataset.shape[1]-6:dataset.shape[1]]
    #Se ignora la posicion dataset.shape[0]-7 porque ahi esta el sujeto, y esta informacion solo importara para dividir esto para FL
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
    X.to_csv('debug.csv', index=False,header=True)
    # Load and compile Keras model
    model=tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense((20), activation='relu',input_shape = (dataset.shape[1]-7,)))
    model.add(tf.keras.layers.Dense((10), activation='relu'))
    model.add(tf.keras.layers.Dense(6,activation=tf.nn.softmax))
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    fl.client.start_numpy_client("127.0.0.1", client=Client())
