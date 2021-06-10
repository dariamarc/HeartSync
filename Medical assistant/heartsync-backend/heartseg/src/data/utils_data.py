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

def numpy_to_obj(numpy_data):

    verts, faces, normals, values = measure.marching_cubes_lewiner(numpy_data, 0)
    faces = faces + 1

    print(verts)
    print(faces)
    print(normals)
    print(values)

    return verts, faces, normals, values