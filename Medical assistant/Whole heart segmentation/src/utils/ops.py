import h5py
import numpy
import tensorflow


def read_transfer_weights():
    filename = '../model/init/c3d-sports1M_weights.h5'
    f = h5py.File(filename, "r")
    c3d_layers = ['layer_0',
                  'layer_2',
                  'layer_4',
                  'layer_5',
                  'layer_7',
                  'layer_8']
    weights = []

    for layer in c3d_layers:
        param_0 = f[layer]['param_0'][()]
        weights.append([param_0])

    return weights
