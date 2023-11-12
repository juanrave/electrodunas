#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mlflow
import mlflow.sklearn
from pyod.models.iforest import IForest

# defina el servidor para llevar el registro de modelos y artefactos
mlflow.set_tracking_uri('http://localhost:8050')

# registre el experimento
experiment = mlflow.set_experiment("electro dunas")

all_files = glob.glob(os.path.join("/", "*.csv"))

df_from_each_file = (pd.read_csv(f, sep=",") for f in all_files)
df_elec = pd.concat(df_from_each_file, axis=0, ignore_index=True)

data=pd.DataFrame()
X = df_elec[['Active_energy', 'Reactive_energy', 'Voltaje_FA', 'Voltaje_FC']]

with mlflow.start_run(experiment_id=experiment.experiment_id):
    # defina los parámetros del modelo
    outliers_fraction = 0.01 
    random_state = np.random.RandomState(42)
  
    # Cree el modelo con los parámetros definidos y entrénelo
    ift = IForest(contamination=outliers_fraction,random_state=random_state)
    ift.fit(X)

    scores_pred = ift.decision_function(X)
    y_pred = ift.predict(X)
    n_inliers = len(y_pred) - np.count_nonzero(y_pred)
    n_outliers = np.count_nonzero(y_pred == 1)

    # Registre los parámetros
    mlflow.log_param("outliers_fraction", outliers_fraction)
    mlflow.log_param("random_state", random_state)
  
    # Registre el modelo
    mlflow.sklearn.log_model(ift, "IForest")
  
    # Cree y registre la métrica de interés
    mlflow.log_metric("n_outliers", n_outliers)
    mlflow.log_metric("n_inliers", n_inliers)

    print('OUTLIERS : ',n_outliers,'INLIERS : ',n_inliers)
