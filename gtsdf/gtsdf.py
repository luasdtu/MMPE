'''
Created on 12/09/2013

@author: Mads M. Pedersen (mmpe@dtu.dk)
'''
from __future__ import division, print_function, absolute_import, unicode_literals
try:
    import h5py
except ImportError as e:
    raise ImportError("HDF5 library cannot be loaded. Windows XP is a known cause of this problem\n%s" % e)
import os
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass
import numpy as np
import numpy.ma as ma
block_name_fmt = "block%04d"

def load(filename, dtype=None):
    """
    load a General Time Series Data Format - datafile
    =================================================

    Parameters
    ----------

    filename : str or open h5py.File object
        filename or open file object

    dtype: numpy dtype
        type of returned data array, e.g. float16, float32 or float64.
        If None(default) the type of the returned data depends on the type of the file data

    Returns
    -------
    numpy array (dtype=float64, size=no_observations)
        time

    numpy array (dtype=dtype, size = no_observations x no_attributes)
        data

    dict
        info containing:
            - type: "General Time Series Data Format"
            - name: name of dataset or filename if not present in file
            - [description]: description of dataset or "" if not present in file
            - [attribute_names]: list of attribute names
            - [attribute_units]: list of attribute units
            - [attribute_descriptions]: list of attribute descriptions

    """
    if isinstance(filename, h5py.File):
        f = filename
        filename = f.filename
    else:
        f = h5py.File(filename, 'r')

    try:


        info = dict(f.attrs.items())
        check_type(f)
        if (block_name_fmt % 0) not in f:
            raise ValueError("HDF5 file must contain a group named '%s'" % (block_name_fmt % 0))
        block0 = f[block_name_fmt % 0]
        if 'data' not in block0:
            raise ValueError("group %s must contain a dataset called 'data'" % (block_name_fmt % 0))
        _, no_attributes = block0['data'].shape
        if 'name' not in info:
            info['name'] = os.path.splitext(os.path.basename(filename))[0]
        info['description'] = f.attrs.get('description', "")
        if 'attribute_names' in f:
            info['attribute_names'] = f['attribute_names'][:]
        if 'attribute_units' in f:
            info['attribute_units'] = f['attribute_units'][:]
        if 'attribute_descriptions' in f:
            info['attribute_descriptions'] = f['attribute_descriptions'][:]
        no_blocks = f.attrs['no_blocks']

        if dtype is None:
            file_dtype = f[block_name_fmt % 0]['data'].dtype
            if "float" in str(file_dtype):
                dtype = file_dtype
            elif file_dtype in [np.int8, np.uint8, np.int16, np.uint16]:
                dtype = np.float32
            else:
                dtype = np.float64
        data = np.empty((0, no_attributes), dtype=dtype)
        time = np.empty((0), dtype=np.float64)
        for i in range(no_blocks):
            block = f[block_name_fmt % i]
            no_observations, no_attributes = block['data'].shape
            block_time = (block.get('time', np.arange(no_observations))[:]).astype(np.float64)
            if 'time_step' in block.attrs:
                block_time *= block.attrs['time_step']
            if 'time_start' in block.attrs:
                block_time += block.attrs['time_start']
            time = np.append(time, block_time)

            block_data = block['data'][:].astype(dtype)
            if "int" in str(block['data'].dtype):
                block_data[block_data == np.iinfo(block['data'].dtype).max] = np.nan

            if 'gains' in block:
                block_data *= block['gains'][:]
            if 'offsets' in block:
                block_data += block['offsets'][:]
            data = np.append(data, block_data, 0)

        f.close()
        return time, data.astype(dtype), info
    except (ValueError, AssertionError):
        f.close()
        raise



def save(filename, data, **kwargs):
    """
    Save a General Time Series Data Format - datafile
    =================================================

    Parameters
    ----------
    - filename
    - data [numpy array size no_observations x no_attributes]
    - kwargs *optional* arguments:
        - name [str]
        - description [str]
        - attribute_names [list with no_attributes strings]
        - attribute_units [list with no_attributes strings]
        - attribute_descriptions [list with no_attributes strings]
        - time [numpy array size no_observations], default=0..no_observations-1
        - time_step (e.g. 1/sample frequency), [int or float type], default=1
        - time_start (e.g. start time in seconds since 1/1/1970), [int or float type], default=0
        - dtype [numpy.dtype], data type of saved data array, default uint16
    """

    if not filename.lower().endswith('.hdf5'):
        filename += ".hdf5"
    f = h5py.File(filename, "w")
    try:
        f.attrs["type"] = "General time series data format"
        no_observations, no_attributes = data.shape
        if 'name' in kwargs:
            f.attrs['name'] = kwargs['name']
        if 'description' in kwargs:
            f.attrs['description'] = kwargs['description']
        f.attrs['no_attributes'] = no_attributes
        if 'attribute_names' in kwargs:
            assert(len(kwargs['attribute_names']) == no_attributes)
            f.create_dataset("attribute_names", data=np.array(kwargs['attribute_names'], dtype=np.string_))
        if 'attribute_units' in kwargs:
            assert(len(kwargs['attribute_units']) == no_attributes)
            f.create_dataset("attribute_units", data=np.array(kwargs['attribute_units'], dtype=np.string_))
        if 'attribute_descriptions' in kwargs:
            assert(len(kwargs['attribute_descriptions']) == no_attributes)
            f.create_dataset("attribute_descriptions", data=np.array(kwargs['attribute_descriptions'], dtype=np.string_))
        f.attrs['no_blocks'] = 0
        f.close()
        append_block(filename, data, **kwargs)
    except AssertionError:
        f.close()
        raise

def append_block(filename, data, **kwargs):
    try:
        f = h5py.File(filename, "a")
        check_type(f)
        no_observations, no_attributes = data.shape
        assert(no_attributes == f.attrs['no_attributes'])
        blocknr = f.attrs['no_blocks']
        if blocknr == 0:
            dtype = kwargs.get('dtype', np.uint16)
        else:
            dtype = f[block_name_fmt % 0]['data'].dtype

        block = f.create_group(block_name_fmt % blocknr)
        if 'time' in kwargs:
            assert(len(kwargs['time']) == no_observations)
            block.create_dataset('time', data=kwargs['time'])
        if 'time_step' in kwargs:
            time_step = kwargs['time_step']
            block.attrs['time_step'] = time_step
        if 'time_start' in kwargs:
            block.attrs['time_start'] = kwargs['time_start']

        pct_res = np.array([1])
        if "int" in str(dtype):
            if np.any(np.isinf(data)):
                f.close()
                raise ValueError ("Int compression does not support 'inf'\nConsider removing outliers or use float datatype")
            nan = np.isnan(data)
            non_nan_data = ma.masked_array(data, nan)
            offsets = np.min(non_nan_data, 0)
            data = np.copy(data)
            data -= offsets
            with np.errstate(invalid='ignore'):  # ignore warning caused by abs(nan)
                pct_res = (np.percentile(data, 75, 0) - np.percentile(data, 25, 0)) / np.nanmax(np.abs(data), 0)  # percent of resolution for middle half of data
            gains = np.max(non_nan_data - offsets, 0).astype(np.float64) / (np.iinfo(dtype).max - 1)  #-1 to save value for NaN
            not0 = np.where(gains != 0)
            data[:, not0] /= gains[not0]

            data = data.astype(dtype)
            data[nan] = np.iinfo(dtype).max

            block.create_dataset('gains', data=gains)
            block.create_dataset('offsets', data=offsets)

        block.create_dataset("data", data=data.astype(dtype))
        f.attrs['no_blocks'] = blocknr + 1
        f.close()

        if "int" in str(dtype):
            int_res = (np.iinfo(dtype).max - np.iinfo(dtype).min)
            if min(pct_res[pct_res > 0]) * int_res < 256:
                raise Warning("Less than 256 values are used to represent 50%% of the values in column(s): %s\nConsider removing outliers or use float datatype" % np.where(pct_res[pct_res > 0] * int_res < 256)[0])

    except AssertionError:
        f.close()
        raise


def check_type(f):
    if 'type' not in f.attrs or f.attrs['type'].lower() != "general time series data format":
        raise ValueError("HDF5 file must contain a 'type'-attribute with the value 'General time series data format'")
    if 'no_blocks' not in f.attrs:
        raise ValueError("HDF5 file must contain an attribute named 'no_blocks'")
