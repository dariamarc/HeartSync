import logging

import numpy as np
from matplotlib import pyplot as plt

from src.data.load_data import DataLoader
from src.data.transform_data import preprocess_data
from src.data.utils_data import show_slices, save_image_file
from src.model.model import UnetModel

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    model = UnetModel('heartseg_model_v3.h5')
    # model.train_model()
    data_loader = DataLoader()
    test_images, labesl = data_loader.load_training_data_clahe()
    for i in range(len(test_images)):
        predictions = model.test_model(test_images[i])
    #     print(predictions)
    #     # save_image_file(predictions)
    #     # predictions = np.reshape(predictions, (64, 64, 64))
    #     print(predictions.shape)
    #     print(predictions.min())
    #     print(predictions.max())

        sh = predictions.shape
        slice0 = predictions[sh[0] // 2, :, :]
        slice1 = predictions[:, sh[1] // 2, :]
        slice2 = predictions[:, :, sh[2] // 2]

        show_slices([slice0, slice1])

        sh = labesl[i].shape
        slice0 = labesl[i][sh[0] // 2, :, :]
        slice1 = labesl[i][:, sh[1] // 2, :]
        slice2 = labesl[i][:, :, sh[2] // 2]

        show_slices([slice0, slice1])



