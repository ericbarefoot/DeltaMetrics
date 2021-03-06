import pytest

import sys
import os

import numpy as np

from deltametrics import io

rcm8_path = os.path.join(os.path.dirname(__file__), '..', 'deltametrics',
                         'sample_data', 'files', 'pyDeltaRCM_Output_8.nc')


def test_netcdf_io_init():
    netcdf_io = io.NetCDFIO(data_path=rcm8_path)
    assert netcdf_io.type == 'netcdf'
    assert len(netcdf_io._in_memory_data.keys()) == 0


def test_netcdf_io_keys():
    netcdf_io = io.NetCDFIO(data_path=rcm8_path)
    assert len(netcdf_io.keys) == 11


def test_netcdf_io_nomemory():
    netcdf_io = io.NetCDFIO(data_path=rcm8_path)
    dataset_size = sys.getsizeof(netcdf_io.dataset)
    inmemory_size = sys.getsizeof(netcdf_io._in_memory_data)

    var = 'velocity'
    velocity_arr = netcdf_io.dataset[var][
        :, 10, :]  # slice the dataset directly
    assert len(velocity_arr.shape) == 2
    assert type(velocity_arr) is np.ma.MaskedArray

    dataset_size_after = sys.getsizeof(netcdf_io.dataset)
    inmemory_size_after = sys.getsizeof(netcdf_io._in_memory_data)

    assert dataset_size == dataset_size_after
    assert inmemory_size == inmemory_size_after


@pytest.mark.xfail()
def test_netcdf_io_intomemory_direct():
    netcdf_io = io.NetCDFIO(data_path=rcm8_path)
    dataset_size = sys.getsizeof(netcdf_io.dataset)
    inmemory_size = sys.getsizeof(netcdf_io._in_memory_data)

    var = 'velocity'
    assert len(netcdf_io._in_memory_data.keys()) == 0
    netcdf_io._in_memory_data[var] = np.array(netcdf_io.dataset.variables[var])
    assert len(netcdf_io._in_memory_data.keys()) == 1
    _arr = netcdf_io._in_memory_data[var]

    dataset_size_after = sys.getsizeof(netcdf_io.dataset)
    inmemory_size_after = sys.getsizeof(netcdf_io._in_memory_data)

    assert dataset_size == dataset_size_after
    assert inmemory_size < inmemory_size_after
    assert sys.getsizeof(_arr) > 1000


@pytest.mark.xfail()
def test_netcdf_io_intomemory_read():
    netcdf_io = io.NetCDFIO(data_path=rcm8_path)
    dataset_size = sys.getsizeof(netcdf_io.dataset)
    inmemory_size = sys.getsizeof(netcdf_io._in_memory_data)

    var = 'velocity'
    assert len(netcdf_io._in_memory_data.keys()) == 0
    netcdf_io.read(var)
    assert len(netcdf_io._in_memory_data.keys()) == 1
    _arr = netcdf_io._in_memory_data[var]

    dataset_size_after = sys.getsizeof(netcdf_io.dataset)
    inmemory_size_after = sys.getsizeof(netcdf_io._in_memory_data)

    assert dataset_size == dataset_size_after
    assert inmemory_size < inmemory_size_after
    assert sys.getsizeof(_arr) > 1000
