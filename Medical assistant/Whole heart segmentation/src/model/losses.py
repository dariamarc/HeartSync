import configparser
from keras import backend as K
import tensorflow as tf
import numpy as np

from src.utils.ops import one_hot

def dice_loss(pred, gr_truth):
    """
    Calculate dice loss between predicted labels and ground truth
    :param pred: model predictions
    :param gr_truth: ground truth
    :return: dice loss
    """
    gr_truth = tf.cast(gr_truth, dtype='int32')
    gr_truth = one_hot(gr_truth)
    dice = 0

    for i in range(8):
        top = tf.reduce_mean(pred[:, :, :, :, i] * gr_truth[:, :, :, :, i])
        g = tf.reduce_sum(pred[:, :, :, :, i] * pred[:, :, :, :, i])
        p = tf.reduce_sum(gr_truth[:, :, :, :, i] * gr_truth[:, :, :, :, i])
        dice += 2 * top / (g + p)

    return -dice


def softmax_weighted_loss(pred, gr_truth):
    """
    Calculates softmax weighted loss between predicted labels and ground truth
    :param pred: model predictions
    :param gr_truth: ground_truth
    :return: softmax weighted loss
    """
    gr_truth = tf.cast(gr_truth, dtype='int32')
    gr_truth = one_hot(gr_truth)
    softmax_pred = tf.nn.softmax(pred)
    loss = 0

    for i in range(8):
        gti = gr_truth[:, :, :, :, i]
        predi = softmax_pred[:, :, :, :, i]
        weighted = 1 - (tf.reduce_sum(gti) / tf.reduce_sum(gr_truth))
        loss += -tf.reduce_mean(weighted * gti * tf.math.log(tf.clip_by_value(predi, 0.005, 1)))

    return loss


def loss_fn(gr_truth, pred):
    """
    Hybrid loss function used for training the U-net segmentation model
    :param gr_truth: ground truth
    :param pred: model predictions
    :return: loss value
    """
    return dice_loss(pred, gr_truth) + softmax_weighted_loss(pred, gr_truth)

def dice_coef(y_true, y_pred):
        smooth = 1
        intersection = K.sum(y_true * y_pred, axis=-1)
        suma = (K.sum(K.square(y_true), -1) + K.sum(K.square(y_pred), -1) + smooth)
        return (2 * intersection + smooth) / suma
