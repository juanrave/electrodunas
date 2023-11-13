#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mlflow
import mlflow.sklearn
from pyod.models.abod import ABOD
import pandas as pd
import numpy as np
import glob
import os
from scipy import stats

# defina el servidor para llevar el registro de modelos y artefactos
mlflow.set_tracking_uri('http://localhost:8050')

# registre el experimento
experiment = mlflow.set_experiment("electro dunas ABOD")

all_files = glob.glob(os.path.join(".", "*.csv"))

df_from_each_file = (pd.read_csv(f, sep=",") for f in all_files)
df_elec = pd.concat(df_from_each_file, axis=0, ignore_index=True)

data=pd.DataFrame()
X = df_elec[['Active_energy', 'Reactive_energy', 'Voltaje_FA', 'Voltaje_FC']]

with mlflow.start_run(experiment_id=experiment.experiment_id):
    # defina los parámetros del modelo
    outliers_fraction = 0.01
    neighbors=10
  
    # Cree el modelo con los parámetros definidos y entrénelo
    ift = ABOD(contamination=outliers_fraction, n_neighbors=neighbors)
    ift.fit(X)

    scores_pred = ift.decision_function(X)
    y_pred = ift.predict(X)
    n_inliers = len(y_pred) - np.count_nonzero(y_pred)
    n_outliers = np.count_nonzero(y_pred == 1)
    # Registre los parámetros
    mlflow.log_param("outliers_fraction", outliers_fraction)
    mlflow.log_param("neighbors", neighbors)

    # Registre el modelo
    mlflow.sklearn.log_model(ift, "IForest")
  
    # Cree y registre la métrica de interés
    mlflow.log_metric("n_outliers", n_outliers)
    mlflow.log_metric("n_inliers", n_inliers)

    print('OUTLIERS : ',n_outliers,'INLIERS : ',n_inliers)
