import configparser
import logging
import os
from glob import glob
import nibabel as nib
import numpy as np
from matplotlib import pyplot as plt

from src.data.utils_data import read_h5_file, show_slices


class DataLoader:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../model/init/model.ini')
        self.data_path = config.get('MODEL_INIT', 'DATA_DIR')

    def load_training_data(self):
        """
        Load CT images used for training the model. The data are in 2 h5 files, one file containing the images and the
        other containing the labels
        :return: dictionary of images and dictionary of labels
        """
        f_images = self.data_path + '/train/images.h5'
        f_labels = self.data_path + '/train/labels.h5'

        logging.info("Loading train images...")
        images = read_h5_file(f_images)

        logging.info("Loaded train images successfully")
        logging.info("Loading train labels...")
        labels = read_h5_file(f_labels)

        logging.info("Loaded train labels successfully")

        return images, labels

    def load_training_data_clahe(self):
        """
            Loads CT images and labels used for training the model that had CLAHE applied. The images are of type .nii.gz
            :return: list of all test images
        """
        data_dir = os.path.join('..', 'data')
        all_images = glob(os.path.join(data_dir, 'processed\\clahe', '*_image_lps_clahe.nii'))
        all_labels = [x.replace('_image_lps_clahe.nii', '_label_lps.nii.gz') for x in all_images]
        print(len(all_images), ' matching files found:', all_images[0], all_labels[0])

        images = []
        labels = []

        for i in range(len(all_images)):
            nii_image = nib.load(all_images[i])
            image = nii_image.get_fdata()
            sh = image.shape
            image = np.reshape(image, (sh[0], sh[1], sh[2]))
            images.append(image)

            nii_label = nib.load(all_labels[i])
            label = nii_label.get_fdata()
            labels.append(label)

        logging.info("Loaded train data successfully")

        return images, labels

    def load_testing_data(self):
        """
        Loads CT images used for testing the model. The images are of type .nii.gz
        :return: list of all test images
        """
        data_dir = os.path.join('..', 'data')
        all_images = glob(os.path.join(data_dir, 'raw\\ct_test', '*_image.nii.gz'))
        print(len(all_images), ' matching files found:', all_images[0])

        images = []
        for i in range(len(all_images)):
        # for i in range(1):
            image = nib.load(all_images[i]).get_fdata()
            images.append(image)

        return images
