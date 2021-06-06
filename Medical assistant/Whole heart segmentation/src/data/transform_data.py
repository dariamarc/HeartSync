import logging
import random
import cv2
import numpy as np
import skimage.exposure
from scipy import ndimage
from scipy.ndimage import zoom
from scipy.ndimage import rotate
import tensorflow as tf
from nipype.interfaces.image import Reorient
from src.utils.exception import PreprocessException
import tensorflow_addons as tfa


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


def rotate_image(image, label):
    if np.random.random() > 0.65:
        # print 'rotating patch...'
        rand_angle = [-25, 25]
        np.random.shuffle(rand_angle)
        image = tfa.image.rotate(image, rand_angle[0])
        label = tfa.image.rotate(label, rand_angle[0])
        # image = image.numpy()
        # label - label.numpy()
        # image = rotate(image, angle=rand_angle[0], axes=(1, 0), reshape=False, order=1)
        # label = rotate(label, angle=rand_angle[0], axes=(1, 0), reshape=False, order=0)

    return image, label


def clahe_image(image):
    # TODO: fix the CLAHE technique
    """
    Apply CLAHE to image for equalization
    :param image: image to apply CLAHE to
    :return: image that has CLAHE applied
    """
    image = image / 255
    img = skimage.exposure.equalize_adapthist(image, kernel_size=(8, 8))

    return img


def resize_data(img_data, labels_data, size):
    """
    Resize all images and labels from image list and label list
    :param img_data: list of images
    :param labels_data: list of labels
    :return: list of resized images, list of resized labels, list of resized labels with 0s
    """
    img_data = resize_image(img_data, size)
    lab_data = resize_image(labels_data, size)
    lab_r_data = np.zeros(lab_data.shape, dtype='int32')

    return img_data, lab_data, lab_r_data


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
            # img_data = clahe_image(img_data)
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
