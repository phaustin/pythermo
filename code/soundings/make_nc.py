import numpy as np
import string
import glob
import matplotlib.pyplot as plt
import pickle
import scipy.io as io
import os
import dateutil
import datetime
from netCDF3 import Dataset

def add_dim(ncfile,dim_length,dim_name=None):
    if dim_name is None:
        dim_name='dim_%d' % dim_length
    try:
        ncfile.createDimension(dim_name,dim_length)
    except:
        pass
    return dim_name

def add_var(ncfile,var_name,var_val):
    the_dim='dim_%d' % var_val.shape[0]
    new_var=ncfile.createVariable(var_name,var_val.dtype,(the_dim,'var_cols'))
    new_var[:,:]=var_val[...]
    return new_var
                          
                          
if __name__=='__main__':

    picfile=glob.glob('litt*.pic')[0]
    picfile=open(picfile,'r')
    the_data=pickle.load(picfile)

    picfile.close()
    newDict=the_data['data']

    array_list=[]
    for key,value in newDict.items():
        the_date=dateutil.parser.parse(key)
        array_list.append((the_date,key,value))

    array_list.sort()
    the_dates=[item[1] for item in array_list]

    try:
        ncfile=Dataset('output.nc','ws','NETCDF3_CLASSIC')
    except:
        os.unlink('output.nc')
        ncfile=Dataset('output.nc','ws','NETCDF3_CLASSIC')

    keep_arrays=list()
    array_lengths=list()
    for dt_object,date_name,the_array in array_list:
        print date_name
        np_array=np.frombuffer(the_array.data)
        n_cols=len(the_array.dtype)
        np_array=np.reshape(np_array,(-1,n_cols))
        keep_arrays.append((np_array.shape[0],np_array,date_name))
        array_lengths.append(np_array.shape[0])


    dimnames=[add_dim(ncfile,item[0]) for item in keep_arrays]
    ncfile.createDimension('var_cols',8)
    varnames=[add_var(ncfile,item[2],item[1]) for item in keep_arrays]

    col_names=array_list[0][2].dtype.names
    a=[(item[0],item[1]) for item in array_list[0][2].dtype.fields.items()]
    col_names=[item[0] for item in a]
    col_dtypes=[item[1] for item in a]
    col_units=[item[2] for item in col_dtypes]
    print "col_dtypes: ",col_dtypes
    print "col_units: ",col_units
    col_names=('press','height','temp','dewpt','relh','mixr','drct',\
              'sknt')

    titles=('hPa','height_m','temp_C','dewpt_C','relh_percent','mixr_gperkg',\
            'deg','knot')

    ncfile.units=','.join(titles)
    ncfile.col_names=','.join(col_names)

    ## array_lengths.sort()
    ## array_lengths=set(array_lengths)
    ncfile.close()
    


