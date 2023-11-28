import pickle
import pandas as pd
import json

def predict_perdida_no_tecnica(config):
    ##loading the model from the saved file
    pkl_filename = "pnt.pkl"
    with open(pkl_filename, 'rb') as f_in:
        model = pickle.load(f_in)

    if type(config) == dict:
        df = pd.DataFrame(config)
    else:
        df = config
    
    df['Active_energy'] = scaler.transform(df[['Active_energy']]) 
    y_pred = model.predict(df)
    
    if y_pred == 0:
        return 'Comportamiento normal'
    elif y_pred == 1:
        return 'Posible perdida no tecnica'