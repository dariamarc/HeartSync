import h5py
import numpy as np
import tensorflow as tf

def map_image(image, a, b, new_a, new_b):
    """
    Map image values between -1 and 1 using linear mapping
    :param image: image to be mapped
    :return: mapped image
    """

    mapped_img = (image - new_a) * (b - a) / (new_b - new_a) + a

    return mapped_img

def convert_to_int(image):
    """
    Convert a slice of the image into int values
    :param image: slice of size mxn
    :return: image with values rounded as int
    """
    for i in range(len(image)):
        for j in range(len(image[i])):
            image[i][j] = int(image[i][j])

    return image

def one_hot(v):
    """
    Return a one-hot numpy array of the given array of size 8
    :param v: array to be transformed
    :return: one-hot numpy array of given shape
    """
    v = tf.one_hot(v, 8)
    nump = v.numpy()
    nump = np.reshape(nump, (1, 64, 64, 64, 8))
    return nump

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
