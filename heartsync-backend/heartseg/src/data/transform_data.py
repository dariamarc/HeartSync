import copy
import logging
import numpy as np
from nipype.interfaces.image import Reorient
from skimage.transform import resize
from heartseg.src.utils.exception import PreprocessException


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
    """
    Prepare the test image to be processed by the model
    :param image: test image
    :param input_shape: shape of the resized image
    :return: resized image
    """
    image = resize(image, [64, 64, 64], order=0, preserve_range=True, anti_aliasing=False)
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
            img_data = resize(data[i], [64, 64, 64], order=0, preserve_range=True, anti_aliasing=False)
            lab_data = resize(labels[i], [64, 64, 64], order=0, preserve_range=True, anti_aliasing=False)

            lab_r_data = np.zeros(lab_data.shape, dtype='int32')
            label_r = rename_label(lab_data, lab_r_data, rename_map)


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
