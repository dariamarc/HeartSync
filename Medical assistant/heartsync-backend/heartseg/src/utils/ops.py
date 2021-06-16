import numpy as np
import tensorflow as tf


def one_hot(v):
    """
    Return a one-hot numpy array of the given tensor of size 8
    :param v: array to be transformed
    :return: one-hot numpy array of given shape
    """
    v = tf.one_hot(v, 8)
    nump = v.numpy()
    nump = np.reshape(nump, (1, 64, 64, 64, 8))
    return nump
