# -*- coding: utf-8 -*-
"""ED_ElectroDunas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15laGVyXEEZcLamQnesjGIvP0zw3Oiu20
"""

import pandas as pd
import glob
import os

all_files = glob.glob(os.path.join("datos/", "*.csv"))

df_from_each_file = (pd.read_csv(f, sep=",") for f in all_files)
data   = pd.concat(df_from_each_file, axis=0, ignore_index=True)

data.drop(columns=['Fecha'], inplace=True)
data.head()

data.shape

data.info()

data.describe()

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

sns.set_theme(style="white")
corr = data.corr()

sns.heatmap(corr)