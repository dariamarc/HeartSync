'''
Data augmentation:
    1. Intensity scale and shift
    - intensity values of pixels are divided by 2048 and clamped between -1 and 1
    - random intensity augmentations during training, shift intensity values by [-0.1, 0.1]
    and scale them by [0.9, 1.1]
    2. Rotation
    - randomly rotate the volumes by [-10dg, 10dg] in each dimension
    3. Translation
    4. Scaling
    - in training randomly scale by [0.8, 1.2]
    5. Elastic deformation
    - moving positions on a regular 8x8x8 voxel grid randomly by up to 10 voxels
    - interpolating with 3rd order B-splines
'''
import random
import cv2
import numpy as np
import pandas as pd
import cv2
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
import scipy.ndimage


def prepare_data(data):
    for i in range(len(data)):
        data[i] = data[i] / 2048

    return data


def intensity_augmentation(data):
    img_no = 1
    for image in data:
        print("Intensity augmentation for image " + str(img_no))
        image = image + random.uniform(-0.1, 0.1)
        image = image * random.uniform(0.9, 1.1)
        img_no += 1

    return data


def image_augmentation(data, labels):
    for i in range(len(data)):
        print("Whole image augmentation for image " + str(i + 1))
        image = data[i]
        label = labels[i]

        # scale whole image
        image = image * random.uniform(0.8, 1.2)

        # elastic deformation on image
        # image, label = elastic_transform(image, label, image.shape[1] * 2, image.shape[1] * 0.08, image.shape[1] * 0.08)

        # rotation of image
        degrees = random.randint(-10, 10)
        image = scipy.ndimage.rotate(image, degrees)
        label = scipy.ndimage.rotate(label, degrees)
        # image_center = tuple(np.array(image.shape[1::-1]) / 2)
        # rot_mat = cv2.getRotationMatrix2D(image_center, random.randint(-10, 10), 1.0)
        # image = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        # label = cv2.warpAffine(label, rot_mat, label.shape[1::-1], flags=cv2.INTER_LINEAR)
        data[i] = image
        labels[i] = label

    return data, labels


def elastic_transform(image, label, alpha, sigma, alpha_affine, random_state=None):
    if random_state is None:
        random_state = np.random.RandomState(None)

    shape = image.shape
    shape_size = shape[:2]

    # Random affine
    center_square = np.float32(shape_size) // 2
    square_size = min(shape_size) // 3
    pts1 = np.float32([center_square + square_size, [center_square[0] + square_size, center_square[1] - square_size],
                       center_square - square_size])
    pts2 = pts1 + random_state.uniform(-alpha_affine, alpha_affine, size=pts1.shape).astype(np.float32)
    M = cv2.getAffineTransform(pts1, pts2)
    image = cv2.warpAffine(image, M, shape_size[::-1], borderMode=cv2.BORDER_REFLECT_101)

    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dz = np.zeros_like(dx)

    x, y, z = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]), np.arange(shape[2]))
    indices = np.reshape(y + dy, (-1, 1)), np.reshape(x + dx, (-1, 1)), np.reshape(z, (-1, 1))

    return map_coordinates(image, indices, order=1, mode='reflect').reshape(shape), map_coordinates(label, indices, order=1, mode='reflect').reshape(shape)