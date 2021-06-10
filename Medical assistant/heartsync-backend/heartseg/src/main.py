import logging

import numpy as np

from src.data.load_data import DataLoader
from src.data.transform_data import preprocess_data
from src.data.utils_data import show_slices
from src.model.model import UnetModel

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    model = UnetModel('heartseg_model_v2.h5')
    print("It is running here ok")
    model.train_model()
    # data_loader = DataLoader()
    # test_images = data_loader.load_testing_data()
    # for image in test_images:
    #     predictions = model.test_model(image)
    #     predictions = np.reshape(predictions, (64, 64, 64))
    #     print(predictions.min())
    #     print(predictions.max())

        # sh = predictions.shape
        # slice0 = predictions[sh[0] // 2, :, :]
        # slice1 = predictions[:, sh[1] // 2, :]
        # slice2 = predictions[:, :, sh[2] // 2]
        #
        # show_slices([slice0, slice1])
