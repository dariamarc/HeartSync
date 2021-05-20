import os

import h5py
import matplotlib.pyplot as plt
from glob import glob
import nibabel as nib
from nipype.interfaces.image import Reorient
import numpy as np
import itk
from PIL import Image
from src.data.transform_data import clahe_images

BASE_IMG_PATH = os.path.join('..', 'data')


def reorient_data_to_rai(images, labels):
    reorient = Reorient(orientation='LPS')

    for image in images:
        reorient.inputs.in_file = image
        res = reorient.run()
        image = res.outputs.out_file

    for label in labels:
        reorient.inputs.in_file = label
        res = reorient.run()
        label = res.outputs.out_file

    return images, labels

def load_data():
    f_images = 'images.h5'
    f_labels = 'labels.h5'

    images = {}
    labels = {}

    print("Loading train images...")
    with h5py.File(f_images, "r") as f:
        # List all groups
        a_group_key = list(f.keys())

        # Get the data
        for key in a_group_key:
            data = f[key][()]
            images[int(''.join(list(filter(str.isdigit, key))))] = data

    print("Loaded train images successfully")
    print("Loading train labels...")
    with h5py.File(f_labels, "r") as f:
        # List all groups
        a_group_key = list(f.keys())

        # Get the data
        for key in a_group_key:
            data = f[key][()]
            labels[int(''.join(list(filter(str.isdigit, key))))] = data

    print("Loaded train labels successfully")

    return images, labels


def load_training_data_ct():
    all_images = glob(os.path.join(BASE_IMG_PATH, 'processed\\reoriented\\train', '*_image_lps.nii.gz'))
    all_labels = [x.replace('_image_lps.nii.gz', '_label_lps.nii.gz') for x in all_images]
    print(len(all_images), ' matching files found:', all_images[0], all_labels[0])

    images = []
    labels = []
    loading_bar = list("[....................]")
    loading_idx = 1
    for i in range(len(all_images)):
        nii_image = nib.load(all_images[i])
        nii_image.uncache()
        image = nii_image.get_fdata()

        # sh = image.shape
        # slice0 = image[sh[0] // 2, :, :]
        # slice1 = image[:, sh[1] // 2, :]
        # slice2 = image[:, :, sh[2] // 2]
        #
        # show_slices([slice0, slice1, slice2])
        # plt.suptitle("Slices of image")
        # plt.show()
        #
        images.append(image)
        nii_label = nib.load(all_labels[i])
        nii_label.uncache()
        label = nii_label.get_fdata()
        labels.append(label)

        # print(label.shape)
        # sh = label.shape
        # slice0 = label[sh[0] // 2, :, :]
        # slice1 = label[:, sh[1] // 2, :]
        # slice2 = label[:, :, sh[2] // 2]
        #
        # show_slices([slice0, slice1, slice2])
        # plt.suptitle("Slices of label")
        # plt.show()

        loading_bar[loading_idx] = '#'
        print("".join(loading_bar))
        loading_idx += 1

    # with h5py.File('images.h5') as h5file:
    #     for n, image in enumerate(images):
    #         h5file[f'image{n}'] = image
    #
    # with h5py.File('labels.h5') as h5file:
    #     for n, label in enumerate(labels):
    #         h5file[f'label{n}'] = label
    #images = clahe_images(images)
    return images, labels


def show_slices(slices):
    """ Function to display row of image slices """
    print("Showing slices...")
    fig, axes = plt.subplots(1, len(slices))
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.T, cmap="gray", origin="lower")


def load_testing_data_ct():
    all_images = glob(os.path.join(BASE_IMG_PATH, 'raw\\ct_test', '*_image.nii.gz'))
    print(len(all_images), ' matching files found:', all_images[0])

    images = []
    for i in range(len(all_images)):
        image = nib.load(all_images[i]).get_fdata()
        images.append(image)

    return images


def plot_images(test_image, test_labels):
    print(test_image.shape)
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(48, 24))
    # ax1.imshow(test_image[test_image.shape[0] // 2], cmap='gray')
    # ax1.set_title('Image')
    # ax2.imshow(test_labels[test_image.shape[0] // 2], cmap='gray')
    # ax2.set_title('Labels')
    plt.imshow(test_image[:, :, :, 1])
    plt.imshow(test_labels[:, :, 5])
    plt.show()
