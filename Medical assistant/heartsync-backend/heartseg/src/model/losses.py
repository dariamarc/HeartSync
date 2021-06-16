import tensorflow as tf
import numpy as np
from heartseg.src.utils.ops import one_hot


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
    return 100 * dice_loss(pred, gr_truth) + softmax_weighted_loss(pred, gr_truth)


def dice_coef_binary(y_true, y_pred):
    """
    Binary dice coefficient metric
    :param y_true: the labels ground truth
    :param y_pred: the predicted labels
    :return: dice coefficient value
    """
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()
    intersection = np.sum(y_true_f * y_pred_f)
    smooth = 0.0001
    return (2. * intersection + smooth) / (np.sum(y_true_f) + np.sum(y_pred_f) + smooth)


def dice_coef(y_true, y_pred):
    """
    Multi-class dice coefficient metric
    :param y_true: the labels ground truth
    :param y_pred: the predicted labels
    :return: dice coefficient value
    """
    numLabels = 8
    y_true = tf.cast(y_true, dtype='int32')
    y_true = one_hot(y_true)
    y_pred = y_pred.numpy()

    dice = 0
    for index in range(numLabels):
        dice += dice_coef_binary(y_true[:, :, :, index], y_pred[:, :, :, index])
    return dice / numLabels
