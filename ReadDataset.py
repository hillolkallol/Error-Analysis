from netCDF4 import Dataset
import glob
from os.path import basename
from pyhdf.SD import *
import numpy as np


# ACCESS PREDICTION DATA
prediction = "F:/dataset/rain_data/prediction/2d.20160419-acc/caps_nmmb_rad/ar2016041900.netacc03_010800"
netcdfFile = Dataset(prediction)
rain = netcdfFile.variables['acc03_'][:]
rainData = rain[0, :, :] # this is the two dimensional grid, 1155x1683
print(rainData)


# ACCESS VERIFICATION (REAL) DATA
fileName = 'F:/dataset/rain_data/verification/20160419/ar2016041900.hdfacc03_010800'
# Open file in read-only mode (default)
hdfFile = SD(fileName, SDC.READ)
datasets_dic = hdfFile.datasets()
for idx,sds in enumerate(datasets_dic.keys()):
    print (idx,sds)
sds_obj = hdfFile.select('acc03_') # select sds
data = np.array(sds_obj[0, :, :]) # get sds data
print(data)
print(data.min(), data.max(), data.mean(), data.std()) # finding min, max, mean and std

# rescaling the data
for key, value in sds_obj.attributes().items():
    if key == 'max':
        maxValue = value
    if key == 'min':
        minValue = value
scalef = (maxValue - minValue) / 65534.0
original_data = scalef * (data + 32767) + minValue
print(original_data)