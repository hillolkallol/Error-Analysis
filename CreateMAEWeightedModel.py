import csv
import glob
from os.path import basename
import numpy as np
from netCDF4 import Dataset
import pandas as pd
np.seterr(divide='ignore', invalid='ignore')

dataset = Dataset("mae_weighted_model.nc", "w", format="NETCDF4")
dataset.set_auto_mask(False)

days = dataset.createDimension('days', 39)
time = dataset.createDimension('time', 20)
y_axis = dataset.createDimension('y_axis', 46)
x_axis = dataset.createDimension('x_axis', 67)

days = dataset.createVariable('days', "S10",("days"),zlib=True)
time = dataset.createVariable('time', "S10",("time"),zlib=True)
weighted_model = dataset.createVariable("weighted_model","f4",("days","time","y_axis","x_axis"),zlib=True)
#
# # writing days
# i = 0
# for day in glob.glob("F:/dataset/rain_data/verification/*"):
#     # print(basename(day))
#     days[i] = basename(day)
#     i = i + 1
# print(days[:])
#
# #writing times
# i = 0
# for second in glob.glob("F:/dataset/rain_data/verification/20160421/*"):
#     # print(basename(second).split('_')[1]))
#     time[i] = basename(second).split('_')[1]
#     i = i + 1
# print(time[:])

#reading netcdf
# error_rate_file = "F:/dataset/mae.nc"
# netcdf_error_rate_file = Dataset(error_rate_file)
# Total_MAE = netcdf_error_rate_file.variables['Total_MAE'][:]

MAE = pd.read_csv('MAE_70_25x25.csv', header=None)
# rmse = pd.to_numeric(np.array(MAE[2])[1:]).reshape((46, 67))

#reading netcdf
netcdf_entire_dataset = Dataset("F:/dataset/summing_dataset.nc", "r")
rain_models = netcdf_entire_dataset.variables['summing_models']
days_error_rate_file = netcdf_entire_dataset.variables['days'][:]
time_error_rate_file = netcdf_entire_dataset.variables['time'][:]
models_error_rate_file = netcdf_entire_dataset.variables['models'][:]

with open('random30.csv') as csvf:
    ind30 = csv.reader(csvf)
    indexi30 = list(ind30)
    index30 = indexi30[0]

np.set_printoptions(formatter={'float': '{: 0.4f}'.format})
#days
for i in index30:
    # print('day:', i)
    for j in range(len(time_error_rate_file)):
        # print('time:', j)
        numeratorSum = np.zeros(shape=(46, 67))
        denominatorSum = np.zeros(shape=(46, 67))
        for k in range(1, len(models_error_rate_file)):
            print(i, j, k)
            a = rain_models[i,j,k,:,:]
            b = np.array(pd.to_numeric(MAE[k+1], errors='coerce').fillna(0))[1:].reshape((46, 67))
            b = b + 1
            a[a > 300000] = np.nan
            b[b > 300000] = np.nan
            print(a)
            # print(b)
            if not np.isnan(a).all():
                numerator = np.array(a) / np.array(b)
                denominator = 1 / np.array(b)
                # denominator[denominator > 1000] = 0
                numerator[np.isnan(numerator)] = 0
                numerator[np.isinf(numerator)] = 0
                denominator[np.isnan(denominator)] = 0
                denominator[np.isinf(denominator)] = 0
                # print(numerator)
                # print(b)
                # print(denominator)

                numeratorSum = numeratorSum + numerator
                denominatorSum = denominatorSum + denominator
                # print(numeratorSum)
                # print(denominatorSum)
        n = np.array(numeratorSum / denominatorSum)
        # print(n)
        weighted_model[i,j,:,:] = n
        print(weighted_model[i,j,:,:])