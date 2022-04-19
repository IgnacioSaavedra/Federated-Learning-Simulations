import flwr as fl
import tensorflow as tf
import pandas as pd
from typing import Optional,Tuple,Dict
from openpyxl import load_workbook

#Current number of rounds
global round_counter
round_counter=0
#Total number of rounds
global number_of_rounds
number_of_rounds=3


def get_eval_fn(model):
    """Return an evaluation function for server-side evaluation."""
    data_file="integrated data/readied data.csv"
    # Load data and model here to avoid the overhead of doing it in `evaluate` itself
    dataset = pd.read_csv(data_file, encoding='utf-8')
    X = dataset.iloc[:,0:dataset.shape[1]-7]
    y = dataset.iloc[:,dataset.shape[1]-6:dataset.shape[1]]
    #dataset.shape[0]-7 is the subject, neither a feature nor a label
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
    # The `evaluate` function will be called after every round
    def evaluate(
        weights: fl.common.Weights,
    ) -> Optional[Tuple[float, Dict[str, fl.common.Scalar]]]:
        model.set_weights(weights)  # Update model with the latest parameters
        
        #Get the loss and accuracy
        global round_counter
        global number_of_rounds
        loss, accuracy = model.evaluate(x_test, y_test)
        if round_counter==number_of_rounds:
            global number_of_clients
            results_file="results.csv"
            resultsDF = pd.read_csv(results_file, encoding='utf-8') 
            current_results = {"Accuracy":[accuracy],"Loss":[loss],"Number of Clients":[number_of_clients],"Centralized":["Federated"]}
            current_results = pd.DataFrame(current_results)
            resultsDF=pd.concat([resultsDF,current_results])
            resultsDF.to_csv(results_file, index=False)
            
            
        round_counter=round_counter+1
        
        return loss, {"accuracy": accuracy}
    return evaluate


def main() -> None:
    global number_of_rounds
    # (same arguments as FedAvg here) fl.server.strategy.FedAvg(min_available_clients=3)  
    data_file="integrated data/readied data.csv"
    dataset = pd.read_csv(data_file, encoding='utf-8')
    number_of_labels= dataset.shape[1]-7
    model=tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense((20), activation='relu',input_shape=(number_of_labels,)))
    model.add(tf.keras.layers.Dense((10), activation='relu'))
    model.add(tf.keras.layers.Dense(6,activation=tf.nn.softmax))
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    #min_fit_clients=3 ,initial_parameters=model.get_weights()   parametro de estrategia
    global number_of_clients
    number_of_clients=20
    strategy = fl.server.strategy.FedAvg(min_available_clients=number_of_clients,min_fit_clients=number_of_clients,fraction_eval=0,min_eval_clients=0,eval_fn=get_eval_fn(model),initial_parameters=model.get_weights(),)
    fl.server.start_server("127.0.0.1",config={"num_rounds": 3},strategy=strategy)
   
    
    
if __name__ == "__main__":
    main()