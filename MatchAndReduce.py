import pickle
import tensorflow as tf
from netCDF4 import Dataset
import pickle
import numpy as np
import csv
import Orange as og
import math
import itertools as it
from Orange.data import Domain, Table
import random
from Orange.projection import PCA
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import os

#read MAE and RMSE files
readData = pd.read_csv('Model1_MAE.csv', header=None)

x_axis = pd.to_numeric(np.array(readData[1])[1:])
mae = pd.to_numeric(np.array(readData[2])[1:])

#read MAE and RMSE files
readData2 = pd.read_csv('../PrecipitationPrediction/', header=None)

x_axis = pd.to_numeric(np.array(readData[1])[1:])
mae = pd.to_numeric(np.array(readData[2])[1:])

print(x_axis)
