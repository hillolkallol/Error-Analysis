from numpy import *
import csv
import numpy as np
from netCDF4 import Dataset
import glob
from os.path import basename


##################################################################################################
dataset = Dataset("mae25x25.nc", "w", format="NETCDF4")
dataset.set_auto_mask(False)
# dataset.set_fill_off()
# print (dataset.data_model)

days = dataset.createDimension('days', 39)
time = dataset.createDimension('time', 20)
models = dataset.createDimension('models', 40)
y_axis = dataset.createDimension('y_axis', 46)
x_axis = dataset.createDimension('x_axis', 67)

days = dataset.createVariable('days', "S10",("days"),zlib=True)
time = dataset.createVariable('time', "S10",("time"),zlib=True)
models = dataset.createVariable('models', "S30",("models"),zlib=True)

MAE = dataset.createVariable("MAE","f4",("days","time","models","y_axis","x_axis"),zlib=True)
# R2 = dataset.createVariable("R2","f4",("days","time","models","y_axis","x_axis"),zlib=True)
# RMSE = dataset.createVariable("RMSE","f4",("days","time","models","y_axis","x_axis"),zlib=True)

Total_MAE = dataset.createVariable("Total_MAE","f4",("models","y_axis","x_axis"),zlib=True)
# Total_R2 = dataset.createVariable("Total_R2","f4",("models","y_axis","x_axis"),zlib=True)
# Total_RMSE = dataset.createVariable("Total_RMSE","f4",("models","y_axis","x_axis"),zlib=True)

# writing days
i = 0
for day in glob.glob("F:/dataset/rain_data/verification/*"):
    # print(basename(day))
    days[i] = basename(day)
    i = i + 1
print(days[:])

#writing times
i = 0
for second in glob.glob("F:/dataset/rain_data/verification/20160421/*"):
    # print(basename(second).split('_')[1]))
    time[i] = basename(second).split('_')[1]
    i = i + 1
print(time[:])

# writing models
i = 1
arr = []
arr.insert(0, 'time')
for pred_date in glob.glob("F:/dataset/rain_data/prediction/*"):
    # print(pred_date)
    for core in glob.glob(str(pred_date) + "/*"):
        # print(core)
        string = str(basename(core))
        if not string in arr:
            # print(basename(core))
            arr.append(str(basename(core)))
            models[i] = str(basename(core))
            i = i + 1
print(models[:])
###############################################################################################

with open('F:/dataset/rain_data/index70.csv') as csvf:
    ind70 = csv.reader(csvf)
    indexi70 = list(ind70)
    index70 = indexi70[0]

#append netcdf
append_netcdf = Dataset("mae25x25.nc", "a")
MAE = append_netcdf.variables['MAE']

#reading netcdf
netcdf_entire_dataset = Dataset("F:/dataset/summing_dataset.nc", "r")
rain_models = netcdf_entire_dataset.variables['summing_models']
days_error_rate_file = netcdf_entire_dataset.variables['days'][:]
time_error_rate_file = netcdf_entire_dataset.variables['time'][:]
models_error_rate_file = netcdf_entire_dataset.variables['models'][:]
# print(days_error_rate_file)

np.set_printoptions(formatter={'float': '{: 0.4f}'.format})
for i in index70:
    # print('day: ', i)
    # Verification Data: Real Data: running the loop for every day for a given second
    for j in range(len(time_error_rate_file)):
        # print('second: ', j)
        #reading verification file
        a = rain_models[i, j, 0, :, :]
        a[a > 30000] = np.nan
        original_data = np.array(a)
        # print(original_data)

        # go every folder of every prediction model
        for k in range(1, len(models_error_rate_file)):
            print(i, j, k)
            #reading netcdf
            b = rain_models[i, j, k, :, :]
            b[b > 30000] = np.nan
            rain100 = np.array(b)
            # print(rain100)

            MAE_result = abs(original_data - rain100)
            # print(MAE_result)
            MAE[i, j, k, :, :] = MAE_result
            # print(MAE[i, j, k, :, :])

print(MAE[8, 9, 8, 9, 9])
append_netcdf.close()
