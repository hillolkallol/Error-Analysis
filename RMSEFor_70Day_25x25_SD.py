import numpy as np
import csv
from netCDF4 import Dataset
from sklearn.metrics import *
from numpy import *

#reading netcdf
netcdf_entire_dataset = Dataset("summing_dataset.nc", "r")
rain_models = netcdf_entire_dataset.variables['summing_models']
days_error_rate_file = netcdf_entire_dataset.variables['days'][:]
time_error_rate_file = netcdf_entire_dataset.variables['time'][:]
models_error_rate_file = netcdf_entire_dataset.variables['models'][:]

with open('random70.csv') as csvf:
    ind70 = csv.reader(csvf)
    indexi70 = list(ind70)
    index70 = indexi70[0]

np.set_printoptions(formatter={'float': '{: 0.4f}'.format})
np.seterr(divide='ignore', invalid='ignore')


#creating csv file
check = open('RMSE_70_25x25.csv', 'w')
check.truncate()
# writing the headers
check.write(str('Y'))
check.write(', ')
check.write(str('X'))
check.write(', ')
for i in range(1, len(models_error_rate_file)):
    check.write(str(models_error_rate_file[i]))
    check.write(', ')
check.write('\n')

for y in range(46): # 46 y-coordinates
    # print('model:', i, 'day:', j)
    for x in range(67): # 67 x-coordinates
        check.write(str(y))
        check.write(', ')
        check.write(str(x))
        check.write(', ')
        for i in range(1, len(models_error_rate_file)): # for every model
            countArr = np.zeros(shape=(14, 10)) #count array
            sum = 0
            count = 0

            print('Y:', y, 'X:', x, 'model:', i)
            original_data = []
            rain100 = []
            for d in index70:
                original_data.append(np.array(rain_models[d, :10, 0, y, x]))  # real data
                rain100.append(np.array(rain_models[d, :10, i, y, x]))  # model data
            # rain100[rain100>30000] = np.nan

            # print(sqrt(power(abs(original_data - rain100), 2)))
            # print(original_data)
            # print(rain100)
            a = np.array(power((np.array(original_data) - np.array(rain100)), 2)) # square of the difference
            # print(a[0, 0])

            # print(len(a), len(a[0]))
            # print(a[2,3])
            # print(np.nanmin(a), np.nanmax(a))
            # a[a > 30000] = np.nan
            if not (np.isnan(a).all() and np.isinf(a).all):

                # print('yes')
                # print(MAE[j, k, i, :, :])
                # sum = sum + np.array(a)
                # print(sum)
                countArr = countArr + 1 #counting for all values

                mask = ((np.array(original_data) == 0) & (np.array(rain100) == 0)) | (a == np.inf) | (a == np.nan) # if both real and prediction model has value zero
                # print('mask found:', mask)
                countArr[mask] = countArr[mask] - 1 # doing (-1) for not counting zero values
                # max = np.round(np.nanmax(a), 4)
                # min = np.round(np.nanmin(a), 4)
                # print(min,max)

                a[a == np.nan] = 0
                a[a == np.inf] = 0

                # print(a)
                sum = np.nansum(a) #summing all non-nan values
                    # print(sum)
                count= np.sum(countArr)
                avg = sqrt(sum / count) # root mean square error

                check.write(str(avg))
                check.write(', ')
        check.write('\n')
check.close()

    # # print(sum)
    # avg = np.divide(sum, count)
    # # print(avg)
    # Total_MAE[i, :, :] = avg
    # print(Total_MAE[i, :, :])

# append_netcdf.close()
