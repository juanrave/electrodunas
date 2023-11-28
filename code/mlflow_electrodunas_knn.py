#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mlflow
import mlflow.sklearn
from pyod.models.knn import KNN
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import glob
import os
from scipy import stats

# defina el servidor para llevar el registro de modelos y artefactos
mlflow.set_tracking_uri('http://localhost:8050')

# registre el experimento
experiment = mlflow.set_experiment("electro dunas KNN")

all_files = glob.glob(os.path.join(".", "*.csv"))

df_from_each_file = (pd.read_csv(f, sep=",") for f in all_files)
df_elec = pd.concat(df_from_each_file, axis=0, ignore_index=True)

df_elec['Month'] = df_elec['Fecha'].str.slice(5, 7).str.replace("-", "").astype(int)
X = df_elec[['Month', 'Active_energy']]

scaler = MinMaxScaler()
X['Active_energy'] = scaler.fit_transform(X[['Active_energy']])

with mlflow.start_run(experiment_id=experiment.experiment_id):
    # defina los parámetros del modelo
    outliers_fraction = 0.02
  
    # Cree el modelo con los parámetros definidos y entrénelo
    ift = KNN(method='mean', contamination=outliers_fraction)
    ift.fit(X)

    scores_pred = ift.decision_function(X)
    y_pred = ift.predict(X)
    n_inliers = len(y_pred) - np.count_nonzero(y_pred)
    n_outliers = np.count_nonzero(y_pred == 1)
    # Registre los parámetros
    mlflow.log_param("contamination", outliers_fraction)

    # Registre el modelo
    mlflow.sklearn.log_model(ift, "KNN")
  
    # Cree y registre la métrica de interés
    mlflow.log_metric("n_outliers", n_outliers)
    mlflow.log_metric("n_inliers", n_inliers)

    print('OUTLIERS : ',n_outliers,'INLIERS : ',n_inliers)
