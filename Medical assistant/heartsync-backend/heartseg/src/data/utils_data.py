import matplotlib.pyplot as plt
import h5py
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


def numpy_to_obj(numpy_data):
    """
    Convert 3D numpy array into a 3D mesh
    :param numpy_data: numpy array
    :return: vertices, faces, vector normals and values of the new 3D mesh
    """
    verts, faces, normals, values = measure.marching_cubes_lewiner(numpy_data, 0)
    faces = faces + 1

    return verts, faces, normals, values


