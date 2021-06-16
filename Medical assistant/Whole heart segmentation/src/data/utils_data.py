import copy
import os
from datetime import datetime

import matplotlib.pyplot as plt
import h5py
import numpy as np
from skimage import measure


def read_h5_file(filename):
    """
    Reads contents of h5 file into a dictionary
    :param filename: path to file
    :return: dictionary containing the elements in the file
    """
    elements = {}
    with h5py.File(filename, "r") as f:
        a_group_key = list(f.keys())
        for key in a_group_key:
            data = f[key][()]
            elements[int(''.join(list(filter(str.isdigit, key))))] = data

    return elements


def show_slices(slices):
    """ Function to display row of image slices """
    print("Showing slices...")
    fig, axes = plt.subplots(1, len(slices))
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.T, cmap="gray", origin="lower")

    plt.show()


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

def fit_cube_param(vol_dim, cube_size, ita):
    dim = np.asarray(vol_dim)
    # cube number and overlap along 3 dimensions
    fold = dim / cube_size + ita
    ovlap = np.ceil(np.true_divide((fold * cube_size - dim), (fold - 1)))
    ovlap = ovlap.astype('int')

    fold = np.ceil(np.true_divide((dim + (fold - 1)*ovlap), cube_size))
    fold = fold.astype('int')

    return fold, ovlap

def decompose_data_to_cubes(image, batch_size, input_size, chn_size, ovl):
    cube_list = []
    # get parameters for decompose
    fold, ovlap = fit_cube_param(image.shape, input_size, ovl)
    dim = np.asarray(image.shape)

    for R in range(0, fold[0]):
        r_s = R*input_size - R*ovlap[0]
        r_e = r_s + input_size
        if r_e >= dim[0]:
            r_s = dim[0] - input_size
            r_e = r_s + input_size
        for C in range(0, fold[1]):
            c_s = C*input_size - C*ovlap[1]
            c_e = c_s + input_size
            if c_e >= dim[1]:
                c_s = dim[1] - input_size
                c_e = c_s + input_size
            for H in range(0, fold[2]):
                h_s = H*input_size - H*ovlap[2]
                h_e = h_s + input_size
                if h_e >= dim[2]:
                    h_s = dim[2] - input_size
                    h_e = h_s + input_size
                # partition multiple channels
                cube_temp = image[r_s:r_e, c_s:c_e, h_s:h_e]
                cube_batch = np.zeros([batch_size, input_size, input_size, input_size, chn_size]).astype('float32')
                cube_batch[0, :, :, :, 0] = copy.deepcopy(cube_temp)
                # save
                cube_list.append(cube_batch)

    return cube_list

def compose_cubes_to_vol(cube_list, vol_dim, cube_size, ita, class_n):
    # get parameters for compose
    fold, ovlap = fit_cube_param(vol_dim, cube_size, ita)
    # create label volume for all classes
    map_classes_mat = (np.zeros([vol_dim[0], vol_dim[1], vol_dim[2], class_n])).astype('float32')
    cnt_classes_mat = (np.zeros([vol_dim[0], vol_dim[1], vol_dim[2], class_n])).astype('float32')

    p_count = 0
    for R in range(0, fold[0]):
        r_s = R * cube_size - R * ovlap[0]
        r_e = r_s + cube_size
        if r_e >= vol_dim[0]:
            r_s = vol_dim[0] - cube_size
            r_e = r_s + cube_size
        for C in range(0, fold[1]):
            c_s = C * cube_size - C * ovlap[1]
            c_e = c_s + cube_size
            if c_e >= vol_dim[1]:
                c_s = vol_dim[1] - cube_size
                c_e = c_s + cube_size
            for H in range(0, fold[2]):
                h_s = H * cube_size - H * ovlap[2]
                h_e = h_s + cube_size
                if h_e >= vol_dim[2]:
                    h_s = vol_dim[2] - cube_size
                    h_e = h_s + cube_size
                # accumulation
                map_classes_mat[r_s:r_e, c_s:c_e, h_s:h_e, :] = map_classes_mat[r_s:r_e, c_s:c_e, h_s:h_e, :] + \
                                                                cube_list[p_count]
                cnt_classes_mat[r_s:r_e, c_s:c_e, h_s:h_e, :] = cnt_classes_mat[r_s:r_e, c_s:c_e, h_s:h_e, :] + 1.0

                p_count += 1

    # elinimate NaN
    nan_idx = (cnt_classes_mat == 0)
    cnt_classes_mat[nan_idx] = 1.0
    # average
    compose_vol = map_classes_mat / cnt_classes_mat

    return compose_vol

def numpy_to_obj(numpy_data):

    verts, faces, normals, values = measure.marching_cubes_lewiner(numpy_data, 0)
    faces = faces + 1

    print(verts)
    print(faces)
    print(normals)
    print(values)

    return verts, faces, normals, values

def save_image_file(image):
        verts, faces, normals, values = numpy_to_obj(image)

        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H%M%S")

        filename = 'lucky.obj'
        # path = os.path.join('file\\files\\', filename)
        obj_file = open(filename, 'w')
        for item in verts:
            obj_file.write("v {0} {1} {2}\n".format(item[0], item[1], item[2]))

        for item in normals:
            obj_file.write("vn {0} {1} {2}\n".format(item[0], item[1], item[2]))

        for item in faces:
            obj_file.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0], item[1], item[2]))

        obj_file.close()

