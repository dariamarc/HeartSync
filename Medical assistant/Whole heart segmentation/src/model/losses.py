import tensorflow as tf
import numpy as np


def one_hot(v):
    v = tf.one_hot(v, 8)
    nump = v.numpy()
    nump = np.reshape(nump, (1, 64, 64, 64, 8))
    return nump


def dice_loss(pred, gr_truth):
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
    return dice_loss(pred, gr_truth) + softmax_weighted_loss(pred, gr_truth)