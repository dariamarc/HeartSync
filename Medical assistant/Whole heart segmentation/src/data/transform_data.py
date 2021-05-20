import random
import cv2
import skimage.exposure
from PIL import Image
import numpy as np
from matplotlib import cm
from scipy import ndimage
from scipy.ndimage import zoom
from skimage.transform import resize
import tensorflow as tf


def resize_image(image, resize_factor):
    depth_factor = resize_factor / image.shape[0]
    height_factor = resize_factor / image.shape[1]
    width_factor = resize_factor / image.shape[2]
    resized_image = zoom(image, (depth_factor, height_factor, width_factor))
    return resized_image


def rotate_image(image, label):

    def scipy_rotate(image, label):
        # pick angle at random
        angle = random.randint(-25, 25)
        # rotate volume
        image = ndimage.rotate(image, angle, reshape=False)
        image[image < 0] = 0
        image[image > 1] = 1

        label = ndimage.rotate(label, angle, reshape=False)
        label[label < 0] = 0
        label[label > 1] = 1
        return image, label

    augmented_volume = tf.numpy_function(scipy_rotate, [image, label], tf.float32)
    return augmented_volume


def clahe_images(data):
    for i in range(len(data)):
        data[i] = data[i] / 2048
        img = skimage.exposure.equalize_adapthist(data[i] / 2048, 8)
        data[i] = img

    return data


def resize_data(img_data, labels_data, resize_ratio=0.6):

    # resize_dim = (np.array(img_data.shape) * resize_ratio).astype('int')
    # img_data = resize(img_data, resize_dim, order=1, preserve_range=True)
    # lab_data = resize(labels_data, resize_dim, order=1, preserve_range=True)

    img_data = resize_image(img_data, 64)
    lab_data = resize_image(labels_data, 64)
    lab_r_data = np.zeros(lab_data.shape, dtype='int32')

    return img_data, lab_data, lab_r_data


def rename_label(label, lab_r_data, rename_map):
    for i in range(len(rename_map)):
        lab_r_data[label == rename_map[i]] = i

    return lab_r_data


def preprocess_data(data, labels):
    rename_map = [0, 205, 420, 500, 550, 600, 820, 850]

    images = []
    labels_proc = []

    print("Preparing data for training. This may take a few minutes")
    for i in range(len(data)):
        img_data, label, label_r = resize_data(data[i], labels[i])
        label_r = rename_label(label, label_r, rename_map)
        img_data = normalize_img(img_data)
        images.append(img_data)
        labels_proc.append(label_r)

    print("Finished preparing data for training")
    return images, labels_proc


def normalize_img(img):
    img = img / 255.0
    mean_temp = np.mean(img)
    dev_temp = np.std(img)
    img_norm = (img - mean_temp) / dev_temp
    return img_norm


def transform_data(data, labels, model):
    if model == "localization":
        for i in range(len(data)):
            image = data[i]
            label = labels[i]

            image = image / 2048  # clamp the intensity values between -1 and 1
            image = resize_image(image, 32)
            image = tf.expand_dims(image, axis=3)
            data[i] = image

            label = resize_image(label, 32)
            label = tf.expand_dims(label, axis=3)
            labels[i] = label

        return np.asarray(data), np.asarray(labels)
    elif model == "segmentation":
        for i in range(len(data)):
            image = data[i]
            label = labels[i]

            image = resize_image(image, 64)
            image = tf.expand_dims(image, axis=3)
            data[i] = image

            label = resize_image(label, 64)
            label = tf.expand_dims(label, axis=3)
            labels[i] = label

        return np.asarray(data), np.asarray(labels)
    return None
