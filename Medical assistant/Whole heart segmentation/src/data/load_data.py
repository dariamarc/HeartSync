import configparser
import logging
import os
from glob import glob
import nibabel as nib
from src.data.utils_data import read_h5_file


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

    def load_testing_data(self):
        """
        Loads CT images used for testing the model. The images are of type .nii.gz
        :return: list of all test images
        """
        all_images = glob(os.path.join(self.data_path, 'raw\\ct_test', '*_image.nii.gz'))
        print(len(all_images), ' matching files found:', all_images[0])

        images = []
        for i in range(len(all_images)):
            image = nib.load(all_images[i]).get_fdata()
            images.append(image)

        return images
