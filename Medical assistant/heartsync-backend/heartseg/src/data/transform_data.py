import copy
import logging
import math
import random
import cv2
import numpy as np
import skimage.exposure
from matplotlib import pyplot as plt
from scipy import ndimage
from scipy.ndimage import zoom
from scipy.ndimage import rotate
import tensorflow as tf
from nipype.interfaces.image import Reorient

from heartseg.src.data.utils_data import show_slices
from heartseg.src.utils.exception import PreprocessException
import tensorflow_addons as tfa

from heartseg.src.utils.ops import map_image, convert_to_int


def resize_image(image, resize_factor):
    """
    Resize image by a resize factor on x, y and z axis
    :param image: image to be resized
    :param resize_factor: resize factor used
    :return: resized image
    """
    depth_factor = resize_factor / image.shape[0]
    height_factor = resize_factor / image.shape[1]
    width_factor = resize_factor / image.shape[2]
    resized_image = zoom(image, (depth_factor, height_factor, width_factor))
    return resized_image


def rotate_tf(image, label):
    image, label = tf.py_function(func=rotate_image, inp=[image, label], Tout=tf.float64)
    return image, label

def rotate_images(images, labels):
    n = len(images)

    new_images = []
    new_labels = []
    for i in range(n):
        new_images.append(images[i])

        # img = np.reshape(images[i], (64, 64, 64))
        # sh = img.shape
        # slice0 = img[sh[0] // 2, :, :]
        # slice1 = img[:, sh[1] // 2, :]
        # slice2 = img[:, :, sh[2] // 2]
        #
        # show_slices([slice0, slice1, slice2])
        new_labels.append(labels[i])
        # random augmentation of the current image
        if np.random.random() > 0.65:
            rot_img, rot_label = rotate_image(images[i], labels[i])

        # rot_img = np.reshape(rot_img, (64, 64, 64))
        # sh = rot_img.shape
        # slice0 = rot_img[sh[0] // 2, :, :]
        # slice1 = rot_img[:, sh[1] // 2, :]
        # slice2 = rot_img[:, :, sh[2] // 2]
        #
        # show_slices([slice0, slice1, slice2])
            new_images.append(rot_img)
            new_labels.append(rot_label)

    return new_images, new_labels


def rotate_image(image, label):
    # if np.random.random() > 0.65:
    rand_angle = [-25, 25]
    np.random.shuffle(rand_angle)
        # image = image.numpy()
        # label - label.numpy()
    image = rotate(image, angle=rand_angle[0], axes=(1, 0), reshape=False, order=1)
    label = rotate(label, angle=rand_angle[0], axes=(1, 0), reshape=False, order=0)

        # image = tf.convert_to_tensor(image)
        # label = tf.convert_to_tensor(label)

    return image, label


def resize_data(img_data, labels_data, size):
    """
    Resize all images and labels from image list and label list
    :param img_data: list of images
    :param labels_data: list of labels
    :return: list of resized images, list of resized labels, list of resized labels with 0s
    """
    # img_data = resize_image(img_data, size)
    # lab_data = resize_image(labels_data, size)

    rand_img = img_data.astype('float32')
    rand_label = labels_data.astype('int32')

    # randomly select a box anchor
    l, w, h = rand_img.shape
    l_rand = np.arange(l - size)
    w_rand = np.arange(w - size)
    h_rand = np.arange(h - size)

    cropped = False
    while not cropped:
        np.random.shuffle(l_rand)
        np.random.shuffle(w_rand)
        np.random.shuffle(h_rand)
        pos = np.array([l_rand[0], w_rand[0], h_rand[0]])
        # crop
        img_temp = copy.deepcopy(rand_img[pos[0]:pos[0] + size, pos[1]:pos[1] + size, pos[2]:pos[2] + size])

        label_temp = copy.deepcopy(
            rand_label[pos[0]:pos[0] + size, pos[1]:pos[1] + size, pos[2]:pos[2] + size])

        lenny = len(set(label_temp.flatten()))
        print(lenny)
        if lenny >= 7:
            cropped = True

    lab_r_data = np.zeros(label_temp.shape, dtype='int32')

    return img_temp, label_temp, lab_r_data


def rename_label(label, lab_r_data, rename_map):
    """
    Renames label values to integers from 0 to 7
    :param label: label data
    :param lab_r_data: volume with 0s the same size of label
    :param rename_map: dictionary containing renaming mappings for each label
    :return: label data renamed
    """
    for i in range(len(rename_map)):
        lab_r_data[label == rename_map[i]] = i

    return lab_r_data


def prepare_test_image(image, input_shape):
    image = resize_image(image, input_shape[0])
    image = normalize_img(image)
    image = np.reshape(image, (1, input_shape[0], input_shape[1], input_shape[2], input_shape[3]))

    return image


def preprocess_data(data, labels, input_shape):
    """
    Preprocesses training data: resizing images, renaming the labels, normalizing images, applying CLAHE
    :param data: list of images
    :param labels: list of labels
    :param input_shape: shaoe of the input for the model
    :return: list of processed images and list of processed labels
    """
    rename_map = [0, 205, 420, 500, 550, 600, 820, 850]

    images = []
    labels_proc = []

    logging.info("Preparing data for training. This may take a few minutes")

    for i in range(len(data)):
        try:
            img_data, label, label_r = resize_data(data[i], labels[i], int(input_shape[0]))
            label_r = rename_label(label, label_r, rename_map)
            img_data = normalize_img(img_data)
            images.append(img_data)
            labels_proc.append(label_r)
        except Exception as e:
            raise PreprocessException(e)

    images = np.reshape(images, (len(images), input_shape[0], input_shape[1], input_shape[2], input_shape[3]))
    labels_proc = np.reshape(labels_proc, (len(labels_proc), input_shape[0], input_shape[1], input_shape[2], input_shape[3]))

    logging.info("Finished preparing data for training")
    return images, labels_proc


def normalize_img(img):
    """
    Normalize by mean of pixels given image
    :param img: image to be normalized
    :return: normalized image
    """
    img = img / 255.0
    mean_temp = np.mean(img)
    dev_temp = np.std(img)
    img_norm = (img - mean_temp) / dev_temp
    return img_norm


def reorient_data_to_rai(images, labels):
    """
    Reorients images and labels to RAI format
    :param images: list of images
    :param labels: list of labels
    """
    reorient = Reorient(orientation='LPS')

    for image in images:
        reorient.inputs.in_file = image
        res = reorient.run()
        image = res.outputs.out_file

    for label in labels:
        reorient.inputs.in_file = label
        res = reorient.run()
        label = res.outputs.out_file
